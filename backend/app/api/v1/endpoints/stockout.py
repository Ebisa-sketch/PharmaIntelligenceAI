from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.stockout_service import StockoutService
from app.schemas.forecasting import StockoutRiskResponse
from app.api.dependencies import get_current_user, check_facility_access
from app.models.user import User

router = APIRouter()


@router.get(
    "/facilities/{facility_id}",
    response_model=List[StockoutRiskResponse],
    summary="Evaluate facility stockout risks",
)
def get_facility_stockout_risks(
    facility_id: int,
    risk_level: Optional[str] = Query(None, description="Filter by risk level (Critical, High, Medium, Low)"),
    persist: bool = Query(True, description="Persist evaluated predictions to database"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Evaluates probabilistic stockout risks across all facility medicines:
    - Calculates Days of Stock Remaining (DSR)
    - Compares against procurement lead time
    - Returns calibrated risk probabilities and XAI feature attributions
    """
    if not check_facility_access(current_user, facility_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to requested facility.",
        )

    service = StockoutService(db)
    risks = service.evaluate_facility_stockouts(facility_id, persist=persist)

    if risk_level:
        risks = [r for r in risks if r.risk_level.lower() == risk_level.lower()]

    return risks
