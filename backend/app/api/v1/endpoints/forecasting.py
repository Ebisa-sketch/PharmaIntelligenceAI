from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.forecasting_service import ForecastingService
from app.schemas.forecasting import ForecastRequest, ForecastResponse, ModelComparisonResponse
from app.api.dependencies import get_current_user, check_facility_access
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=ForecastResponse, summary="Generate demand forecast")
def generate_forecast(
    request: ForecastRequest,
    persist: bool = Query(True, description="Persist generated forecast to database"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generates multi-period demand forecasts with prediction intervals (P10, P50, P90)
    and explainable AI diagnostic summaries.
    """
    if not check_facility_access(current_user, request.facility_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to requested facility.",
        )

    service = ForecastingService(db)
    return service.generate_forecast(
        facility_id=request.facility_id,
        medicine_id=request.medicine_id,
        horizon_days=request.horizon_days,
        model_type=request.model_type,
        persist=persist,
    )


@router.get(
    "/facilities/{facility_id}/medicines/{medicine_id}",
    response_model=ForecastResponse,
    summary="Get or generate medicine forecast",
)
def get_forecast(
    facility_id: int,
    medicine_id: int,
    horizon_days: int = Query(90, ge=7, le=365),
    model_type: str = Query("ensemble"),
    persist: bool = Query(True),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieves or calculates demand forecast for a specific medicine at a facility."""
    if not check_facility_access(current_user, facility_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to requested facility.",
        )

    service = ForecastingService(db)
    return service.generate_forecast(
        facility_id=facility_id,
        medicine_id=medicine_id,
        horizon_days=horizon_days,
        model_type=model_type,
        persist=persist,
    )


@router.get(
    "/facilities/{facility_id}/medicines/{medicine_id}/compare",
    response_model=ModelComparisonResponse,
    summary="Benchmark and compare forecasting algorithms",
)
def compare_models(
    facility_id: int,
    medicine_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Classifies demand series via Syntetos-Boylan (ADI, CV^2) and evaluates candidate
    models (Moving Average, Exponential Smoothing, Croston-SBA, Gradient Boosting)
    reporting RMSE, MAE, MAPE, WAPE, and MASE.
    """
    if not check_facility_access(current_user, facility_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to requested facility.",
        )

    service = ForecastingService(db)
    return service.compare_models(facility_id=facility_id, medicine_id=medicine_id)
