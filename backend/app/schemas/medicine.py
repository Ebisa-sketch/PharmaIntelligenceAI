from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class MedicineBase(BaseModel):
    code: str
    name: str
    brand_name: Optional[str] = None
    category: str
    dosage_form: str
    strength: str
    unit_of_measure: str
    is_essential: bool = True
    vital_classification: str = "Essential"
    minimum_stock_level: float = 0.0
    reorder_point: float = 0.0
    lead_time_days: int = 30


class MedicineCreate(MedicineBase):
    pass


class MedicineUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    brand_name: Optional[str] = None
    category: Optional[str] = None
    dosage_form: Optional[str] = None
    strength: Optional[str] = None
    unit_of_measure: Optional[str] = None
    is_essential: Optional[bool] = None
    vital_classification: Optional[str] = None
    minimum_stock_level: Optional[float] = None
    reorder_point: Optional[float] = None
    lead_time_days: Optional[int] = None


class MedicineResponse(MedicineBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BatchBase(BaseModel):
    batch_number: str
    expiry_date: date
    manufacturing_date: Optional[date] = None
    quantity_initial: float
    quantity_remaining: float
    unit_cost_etb: float = 0.0
    status: str = "Active"


class BatchCreate(BatchBase):
    facility_id: int
    medicine_id: int


class BatchResponse(BatchBase):
    id: int
    facility_id: int
    medicine_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
