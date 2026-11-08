from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.redistribution_service import RedistributionService
from app.schemas.recommendation import (
    RedistributionOptimizationRun,
    RedistributionResponse,
    RedistributionDetailResponse,
    RedistributionStatusUpdate,
    SimulationScenarioRequest,
    SimulationScenarioResponse,
)
from app.api.dependencies import get_current_user, require_roles
from app.models.user import User

router = APIRouter()


@router.post("/optimize", response_model=List[RedistributionResponse], summary="Run MILP redistribution optimizer")
def run_optimization(
    params: RedistributionOptimizationRun,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin", "pharmacy_manager"])),
):
    """
    Executes the Mixed-Integer Linear Programming (MILP) redistribution optimization:
    - Protects donor safety stock thresholds
    - Identifies recipient stockout deficits
    - Generates cost-optimal lateral transfer recommendations with shelf-life viability
    """
    service = RedistributionService(db)
    recs = service.optimize_and_generate_recommendations(params)
    return service.get_recommendations()[:len(recs)]


@router.get("/recommendations", response_model=List[RedistributionResponse], summary="List lateral transfer proposals")
def list_recommendations(
    facility_id: Optional[int] = Query(None, description="Filter by source or target facility"),
    status: Optional[str] = Query(None, description="Pending, Approved, Rejected, Completed"),
    priority: Optional[str] = Query(None, description="High, Medium, Low"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Lists proposed lateral stock redistribution transfers with filtering."""
    service = RedistributionService(db)
    return service.get_recommendations(
        facility_id=facility_id,
        status=status,
        priority=priority,
        skip=skip,
        limit=limit,
    )


@router.get("/recommendations/{recommendation_id}", response_model=RedistributionDetailResponse, summary="Get proposal with mathematical proof")
def get_recommendation_detail(
    recommendation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieves full recommendation details including mathematical constraints verification proof."""
    service = RedistributionService(db)
    return service.get_recommendation_detail(recommendation_id)


@router.patch("/recommendations/{recommendation_id}/approve", response_model=RedistributionDetailResponse, summary="Approve transfer proposal")
def approve_recommendation(
    recommendation_id: int,
    update_in: Optional[RedistributionStatusUpdate] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin", "pharmacy_manager"])),
):
    """Approves a lateral transfer proposal, reserving stock at the donor facility."""
    service = RedistributionService(db)
    rationale = update_in.rationale if update_in else None
    return service.approve_recommendation(
        recommendation_id=recommendation_id,
        user_id=current_user.id,
        rationale=rationale,
    )


@router.patch("/recommendations/{recommendation_id}/reject", response_model=RedistributionDetailResponse, summary="Reject transfer proposal")
def reject_recommendation(
    recommendation_id: int,
    update_in: RedistributionStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin", "pharmacy_manager"])),
):
    """Rejects a lateral transfer proposal with mandatory clinical justification."""
    service = RedistributionService(db)
    reason = update_in.rationale or "Clinical rejection: Transfer not feasible."
    return service.reject_recommendation(
        recommendation_id=recommendation_id,
        user_id=current_user.id,
        reason=reason,
    )


@router.post("/recommendations/{recommendation_id}/execute", response_model=RedistributionDetailResponse, summary="Execute physical inventory transfer")
def execute_transfer(
    recommendation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin", "pharmacy_manager"])),
):
    """Executes inventory transfer: moves physical stock and records bin-card ledgers."""
    service = RedistributionService(db)
    return service.execute_transfer(
        recommendation_id=recommendation_id,
        user_id=current_user.id,
    )


@router.post("/simulate", response_model=SimulationScenarioResponse, summary="Simulate what-if redistribution policies")
def run_simulation(
    request: SimulationScenarioRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Evaluates what-if supply chain policy scenarios:
    - baseline_isolated: Independent facility operation
    - collaborative_network: Multi-facility regional sharing
    - local_cluster: Primary clinic cluster redistribution (40 km radius)
    - epidemic_spike: Outbreak demand surge response evaluation
    """
    service = RedistributionService(db)
    return service.run_simulation(request)
