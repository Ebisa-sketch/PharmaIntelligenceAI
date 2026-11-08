from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.redistribution_service import RedistributionService
from app.services.audit_service import AuditService
from app.repositories.prediction_repository import PredictionRepository
from app.schemas.recommendation import (
    RedistributionOptimizationRun,
    RedistributionResponse,
    RedistributionStatusUpdate,
)
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/optimize", response_model=List[RedistributionResponse])
def run_optimization(
    params: RedistributionOptimizationRun,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = RedistributionService(db)
    results = service.optimize_and_generate_recommendations(params)
    AuditService.log_action(
        db,
        action="RUN_REDISTRIBUTION_OPTIMIZER",
        entity_type="Recommendation",
        user_id=current_user.id,
        details={"region": params.region, "generated_count": len(results)},
    )
    return results


@router.get("/recommendations", response_model=List[RedistributionResponse])
def list_recommendations(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = PredictionRepository(db)
    return repo.get_recommendations(status=status, priority=priority, skip=skip, limit=limit)


@router.put("/recommendations/{recommendation_id}/status", response_model=RedistributionResponse)
def update_recommendation_status(
    recommendation_id: int,
    update_in: RedistributionStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = PredictionRepository(db)
    updated = repo.update_recommendation_status(
        recommendation_id=recommendation_id,
        status=update_in.status,
        reviewer_id=current_user.id,
        rationale=update_in.rationale,
    )
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recommendation not found")

    AuditService.log_action(
        db,
        action=f"REDISTRIBUTION_{update_in.status.upper()}",
        entity_type="Recommendation",
        user_id=current_user.id,
        entity_id=str(recommendation_id),
        details={"new_status": update_in.status, "rationale": update_in.rationale},
    )
    return updated
