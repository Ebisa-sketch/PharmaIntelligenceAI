from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class RedistributionRequest(BaseModel):
    source_facility_id: int
    target_facility_id: int
    medicine_id: int
    batch_id: Optional[int] = None
    quantity_recommended: float
    priority: str = "Medium"
    rationale: str


class RedistributionStatusUpdate(BaseModel):
    status: str  # Approved, Rejected, In_Transit, Completed
    rationale: Optional[str] = None


class RedistributionOptimizationRun(BaseModel):
    region: Optional[str] = None
    max_distance_km: float = 150.0
    min_expiry_months: int = 3
    priority_level: Optional[str] = None


class RedistributionResponse(BaseModel):
    id: int
    source_facility_id: int
    target_facility_id: int
    medicine_id: int
    batch_id: Optional[int] = None
    quantity_recommended: float
    transport_distance_km: Optional[float] = None
    estimated_transfer_cost_etb: Optional[float] = None
    prevented_wastage_cost_etb: Optional[float] = None
    status: str
    priority: str
    rationale: str
    reviewed_by: Optional[int] = None
    reviewed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
