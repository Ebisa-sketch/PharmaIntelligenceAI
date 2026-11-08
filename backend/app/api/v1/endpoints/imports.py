from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.import_service import ImportService
from app.api.dependencies import get_current_user, check_facility_access
from app.models.user import User
from app.models.data_import import DataImport
from app.schemas.data_import import DataImportResponse, DataImportDetailResponse, IngestionPreviewResult

router = APIRouter()


@router.post("/preview", response_model=IngestionPreviewResult, summary="Preview and validate file structure")
async def preview_data_file(
    file: UploadFile = File(...),
    preview_limit: int = Form(5),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Inspects a CSV or Excel file structure, column headers, and data quality issues without committing changes."""
    content = await file.read()
    service = ImportService(db)
    return service.preview_import(content, filename=file.filename or "upload.csv", preview_limit=preview_limit)


@router.post("/inventory-batches", response_model=Dict[str, Any], summary="Import inventory batches (CSV or Excel)")
async def import_inventory_batches(
    facility_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Ingests batch stock levels, calculates DQI, and reconciles inventory balances."""
    if not check_facility_access(current_user, facility_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to manage this facility's inventory."
        )

    content = await file.read()
    service = ImportService(db)
    return service.import_inventory_batches(
        file_bytes=content,
        filename=file.filename or "inventory_batches.csv",
        facility_id=facility_id,
        user_id=current_user.id,
    )


@router.post("/transactions", response_model=Dict[str, Any], summary="Import transaction ledgers (CSV or Excel)")
async def import_inventory_transactions(
    facility_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Ingests historical bin-card transactions (Receipts, Issues, Adjustments, Transfers, Wastage)."""
    if not check_facility_access(current_user, facility_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to manage this facility's records."
        )

    content = await file.read()
    service = ImportService(db)
    return service.import_transactions(
        file_bytes=content,
        filename=file.filename or "transactions.csv",
        facility_id=facility_id,
        user_id=current_user.id,
    )


@router.get("/history", response_model=List[DataImportResponse], summary="List import history")
def get_import_history(
    facility_id: Optional[int] = Query(None, description="Filter by facility"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Lists historical data import jobs and their recorded data quality metrics."""
    query = db.query(DataImport)
    if facility_id:
        if not check_facility_access(current_user, facility_id):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied.")
        query = query.filter(DataImport.facility_id == facility_id)
    elif current_user.facility_id:
        query = query.filter(DataImport.facility_id == current_user.facility_id)

    imports = query.order_by(DataImport.id.desc()).offset(skip).limit(limit).all()
    results = []
    for item in imports:
        results.append(
            DataImportResponse(
                id=item.id,
                facility_id=item.facility_id,
                facility_name=item.facility.name if item.facility else None,
                filename=item.filename,
                file_hash_sha256=item.file_hash_sha256,
                total_rows=item.total_rows,
                valid_rows=item.valid_rows,
                rejected_rows=item.rejected_rows,
                dq_score=item.dq_score,
                status=item.status,
                created_at=item.created_at,
                quality_issues_count=len(item.quality_issues),
            )
        )
    return results


@router.get("/{import_id}", response_model=DataImportDetailResponse, summary="Get import details & issues")
def get_import_detail(
    import_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieves full details of a specific data import run and all logged data quality issues."""
    data_import = db.get(DataImport, import_id)
    if not data_import:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Import #{import_id} not found.")

    if not check_facility_access(current_user, data_import.facility_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied.")

    return DataImportDetailResponse(
        id=data_import.id,
        facility_id=data_import.facility_id,
        facility_name=data_import.facility.name if data_import.facility else None,
        filename=data_import.filename,
        file_hash_sha256=data_import.file_hash_sha256,
        total_rows=data_import.total_rows,
        valid_rows=data_import.valid_rows,
        rejected_rows=data_import.rejected_rows,
        dq_score=data_import.dq_score,
        status=data_import.status,
        created_at=data_import.created_at,
        quality_issues_count=len(data_import.quality_issues),
        quality_issues=[
            {
                "id": issue.id,
                "row_number": issue.row_number,
                "issue_type": issue.issue_type,
                "severity": issue.severity,
                "field_name": issue.field_name,
                "description": issue.description,
                "is_resolved": issue.is_resolved,
            }
            for issue in data_import.quality_issues
        ],
    )
