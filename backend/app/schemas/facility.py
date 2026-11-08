from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class FacilityBase(BaseModel):
    code: str
    name: str
    facility_type: str
    region: str
    zone: Optional[str] = None
    woreda: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    storage_capacity_m3: Optional[float] = None
    is_active: bool = True


class FacilityCreate(FacilityBase):
    pass


class FacilityUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    facility_type: Optional[str] = None
    region: Optional[str] = None
    zone: Optional[str] = None
    woreda: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    storage_capacity_m3: Optional[float] = None
    is_active: Optional[bool] = None


class FacilityResponse(FacilityBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
