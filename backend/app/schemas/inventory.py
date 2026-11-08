from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class InventoryBase(BaseModel):
    facility_id: int
    medicine_id: int
    current_stock: float = 0.0
    reserved_stock: float = 0.0
    usable_stock: float = 0.0
    average_monthly_consumption: float = 0.0
    months_of_stock: float = 0.0
    stock_status: str = "Adequate"


class InventoryUpdate(BaseModel):
    current_stock: Optional[float] = None
    reserved_stock: Optional[float] = None
    usable_stock: Optional[float] = None
    average_monthly_consumption: Optional[float] = None
    stock_status: Optional[str] = None


class InventoryResponse(InventoryBase):
    id: int
    last_counted_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TransactionCreate(BaseModel):
    facility_id: int
    medicine_id: int
    batch_id: Optional[int] = None
    transaction_type: str  # Receipt, Issue, Adjustment_Positive, Adjustment_Negative, Transfer_In, Transfer_Out, Disposal
    quantity: float
    reference_number: Optional[str] = None
    notes: Optional[str] = None


class TransactionResponse(TransactionCreate):
    id: int
    transaction_date: datetime
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
