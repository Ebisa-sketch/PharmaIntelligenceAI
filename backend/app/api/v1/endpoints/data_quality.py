from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.data_quality_service import DataQualityService
from app.api.dependencies import get_current_user, require_roles, check_facility_access
from app.models.user import User
from app.schemas.data_quality import (
    DataQualityAssessmentResponse,
    DataQualityIssueItem,
    IssueResolutionRequest,
)

router = APIRouter()


@router.get(
    "/facilities/{facility_id}/assessment",
    response_model=DataQualityAssessmentResponse,
    summary="Run DQI assessment for a facility",
)
def assess_facility_data_quality(
    facility_id: int,
    persist: bool = Query(True, description="Persist discovered issues to DB"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Runs a comprehensive 5-dimension Data Quality Index (DQI) assessment:
    Completeness, Consistency, Plausibility, Expiry Validity, Uniqueness.
    Returns weighted DQI score and per-dimension breakdown.
    """
    if not check_facility_access(current_user, facility_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to the requested facility.",
        )

    service = DataQualityService(db)
    result = service.assess_facility_data_quality(
        facility_id, persist_issues=persist
    )
    return DataQualityAssessmentResponse(**result)


@router.get(
    "/issues",
    response_model=List[DataQualityIssueItem],
    summary="List data quality issues with filters",
)
def list_data_quality_issues(
    facility_id: Optional[int] = Query(None),
    import_id: Optional[int] = Query(None),
    severity: Optional[str] = Query(None, description="CRITICAL, WARNING, INFO"),
    is_resolved: Optional[bool] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Returns paginated list of logged data quality issues, filterable by facility, import job, severity, and resolution status."""
    if facility_id and not check_facility_access(current_user, facility_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied."
        )

    service = DataQualityService(db)
    issues = service.get_quality_issues(
        facility_id=facility_id,
        import_id=import_id,
        severity=severity,
        is_resolved=is_resolved,
        skip=skip,
        limit=limit,
    )

    results = []
    for issue in issues:
        results.append(
            DataQualityIssueItem(
                id=issue.id,
                import_id=issue.import_id,
                facility_id=issue.facility_id,
                facility_name=issue.facility.name if issue.facility else None,
                medicine_id=issue.medicine_id,
                medicine_name=issue.medicine.name if issue.medicine else None,
                issue_type=issue.issue_type,
                severity=issue.severity,
                field_name=issue.field_name,
                row_number=issue.row_number,
                description=issue.description,
                details=issue.details,
                is_resolved=issue.is_resolved,
                created_at=issue.created_at,
            )
        )
    return results


@router.patch(
    "/issues/{issue_id}/resolve",
    response_model=DataQualityIssueItem,
    summary="Resolve a data quality issue",
)
def resolve_quality_issue(
    issue_id: int,
    body: IssueResolutionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Marks a specific data quality issue as resolved, with optional resolution notes."""
    service = DataQualityService(db)
    issue = service.resolve_issue(issue_id, notes=body.resolution_notes)
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Issue #{issue_id} not found.",
        )

    if not check_facility_access(current_user, issue.facility_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied."
        )

    return DataQualityIssueItem(
        id=issue.id,
        import_id=issue.import_id,
        facility_id=issue.facility_id,
        facility_name=issue.facility.name if issue.facility else None,
        medicine_id=issue.medicine_id,
        medicine_name=issue.medicine.name if issue.medicine else None,
        issue_type=issue.issue_type,
        severity=issue.severity,
        field_name=issue.field_name,
        row_number=issue.row_number,
        description=issue.description,
        details=issue.details,
        is_resolved=issue.is_resolved,
        created_at=issue.created_at,
    )
