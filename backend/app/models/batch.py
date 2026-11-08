from datetime import date
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import CheckConstraint, Date, Float, ForeignKey, Index, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.facility import Facility
    from app.models.medicine import Medicine
    from app.models.transaction import InventoryTransaction
    from app.models.prediction import Prediction
    from app.models.recommendation import RedistributionRecommendation


class Batch(Base, TimestampMixin):
    __tablename__ = "batches"
    __table_args__ = (
        UniqueConstraint("facility_id", "medicine_id", "batch_number", name="uq_facility_medicine_batch"),
        CheckConstraint("quantity_initial >= 0", name="ck_batch_quantity_initial_non_negative"),
        CheckConstraint("quantity_remaining >= 0", name="ck_batch_quantity_remaining_non_negative"),
        CheckConstraint("unit_cost_etb >= 0", name="ck_batch_unit_cost_non_negative"),
        Index("ix_batches_facility_expiry", "facility_id", "expiry_date"),
        Index("ix_batches_medicine_expiry", "medicine_id", "expiry_date"),
        Index("ix_batches_status_expiry", "status", "expiry_date"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    facility_id: Mapped[int] = mapped_column(Integer, ForeignKey("facilities.id", ondelete="CASCADE"), nullable=False, index=True)
    medicine_id: Mapped[int] = mapped_column(Integer, ForeignKey("medicines.id", ondelete="CASCADE"), nullable=False, index=True)
    batch_number: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    expiry_date: Mapped[date] = mapped_column(Date, index=True, nullable=False)
    manufacturing_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    quantity_initial: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    quantity_remaining: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    unit_cost_etb: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)  # Ethiopian Birr
    status: Mapped[str] = mapped_column(String(50), default="Active", nullable=False, index=True)  # Active, Quarantined, Expired, Depleted

    facility: Mapped["Facility"] = relationship("Facility", back_populates="batches")
    medicine: Mapped["Medicine"] = relationship("Medicine", back_populates="batches")
    transactions: Mapped[List["InventoryTransaction"]] = relationship("InventoryTransaction", back_populates="batch")
    predictions: Mapped[List["Prediction"]] = relationship("Prediction", back_populates="batch")
    recommendations: Mapped[List["RedistributionRecommendation"]] = relationship("RedistributionRecommendation", back_populates="batch")
