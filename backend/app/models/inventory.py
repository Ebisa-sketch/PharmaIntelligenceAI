from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import CheckConstraint, DateTime, Float, ForeignKey, Index, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.facility import Facility
    from app.models.medicine import Medicine


class Inventory(Base, TimestampMixin):
    __tablename__ = "inventories"
    __table_args__ = (
        UniqueConstraint("facility_id", "medicine_id", name="uq_facility_medicine_inventory"),
        CheckConstraint("current_stock >= 0", name="ck_inventory_current_stock_non_negative"),
        CheckConstraint("usable_stock >= 0", name="ck_inventory_usable_stock_non_negative"),
        Index("ix_inventory_facility_status", "facility_id", "stock_status"),
        Index("ix_inventory_medicine", "medicine_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    facility_id: Mapped[int] = mapped_column(Integer, ForeignKey("facilities.id", ondelete="CASCADE"), nullable=False, index=True)
    medicine_id: Mapped[int] = mapped_column(Integer, ForeignKey("medicines.id", ondelete="CASCADE"), nullable=False, index=True)
    current_stock: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    reserved_stock: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    usable_stock: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    average_monthly_consumption: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    months_of_stock: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    stock_status: Mapped[str] = mapped_column(String(50), default="Adequate", nullable=False, index=True)  # Stockout, Understocked, Adequate, Overstocked
    last_counted_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    facility: Mapped["Facility"] = relationship("Facility", back_populates="inventories")
    medicine: Mapped["Medicine"] = relationship("Medicine", back_populates="inventories")
