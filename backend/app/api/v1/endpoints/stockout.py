from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.stockout_service import StockoutService
from app.schemas.forecasting import StockoutRiskResponse
from app.api.dependencies import get_current_user, check_facility_access
from app.models.user import User

router = APIRouter()


@router.get("/facilities/{facility_id}", response_model=List[StockoutRiskResponse])
def get_facility_stockout_risks(
    facility_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not check_facility_access(current_user, facility_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied to requested facility")

    service = StockoutService(db)
    return service.evaluate_facility_stockouts(facility_id)
