from datetime import date, datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict


class ForecastRequest(BaseModel):
    facility_id: int
    medicine_id: int
    horizon_days: int = 90
    model_type: str = "ensemble"  # ensemble, gradient_boosting, croston_sba, exponential_smoothing, moving_average


class ForecastPoint(BaseModel):
    date: date
    predicted_consumption: float
    confidence_interval_lower: float
    confidence_interval_upper: float


class ForecastResponse(BaseModel):
    id: Optional[int] = None
    facility_id: int
    medicine_id: int
    model_type: str
    forecast_date: date
    target_period_start: date
    target_period_end: date
    forecast_value: float
    confidence_interval_lower: float
    confidence_interval_upper: float
    mape_score: Optional[float] = None
    uncertainty_score: Optional[float] = None
    demand_category: Optional[str] = "smooth"
    adi: Optional[float] = None
    cv2: Optional[float] = None
    metrics: Optional[Dict[str, float]] = None
    explanation: Optional[str] = None
    series: Optional[List[ForecastPoint]] = None

    model_config = ConfigDict(from_attributes=True)


class StockoutRiskResponse(BaseModel):
    facility_id: int
    facility_name: str
    medicine_id: int
    medicine_name: str
    current_stock: float
    projected_daily_consumption: float
    days_until_stockout: float
    stockout_risk_score: float  # 0.0 - 1.0 probability
    risk_level: str  # Critical, High, Medium, Low
    estimated_stockout_date: Optional[date] = None
    key_drivers: List[str] = []
    recommended_action: str
    explanation: Optional[str] = None
    attributions: Optional[List[Dict[str, Any]]] = None

    model_config = ConfigDict(from_attributes=True)


class ExpiryRiskResponse(BaseModel):
    facility_id: int
    facility_name: str
    medicine_id: int
    medicine_name: str
    batch_id: int
    batch_number: str
    expiry_date: date
    quantity_at_risk: float
    estimated_loss_etb: float
    risk_level: str  # Critical, High, Medium, Low
    monthly_consumption_rate: float
    recommended_action: str
    explanation: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ModelComparisonResponse(BaseModel):
    facility_id: int
    medicine_id: int
    demand_category: str
    adi: float
    cv2: float
    recommended_model: str
    models_evaluated: Dict[str, Dict[str, float]]
