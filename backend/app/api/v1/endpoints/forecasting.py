from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.forecasting_service import ForecastingService
from app.schemas.forecasting import ForecastRequest, ForecastResponse
from app.api.dependencies import get_current_user, check_facility_access
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=ForecastResponse)
def generate_forecast(
    request: ForecastRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not check_facility_access(current_user, request.facility_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied to requested facility")

    service = ForecastingService(db)
    return service.generate_forecast(
        facility_id=request.facility_id,
        medicine_id=request.medicine_id,
        horizon_days=request.horizon_days,
        model_type=request.model_type,
    )


@router.get("/facilities/{facility_id}/medicines/{medicine_id}", response_model=ForecastResponse)
def get_forecast(
    facility_id: int,
    medicine_id: int,
    horizon_days: int = 90,
    model_type: str = "ensemble",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not check_facility_access(current_user, facility_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied to requested facility")

    service = ForecastingService(db)
    return service.generate_forecast(
        facility_id=facility_id,
        medicine_id=medicine_id,
        horizon_days=horizon_days,
        model_type=model_type,
    )
