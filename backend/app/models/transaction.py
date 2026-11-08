from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING
from sqlalchemy import DateTime, Float, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.facility import Facility
    from app.models.medicine import Medicine
    from app.models.batch import Batch
    from app.models.user import User
    from app.models.data_import import DataImport


class InventoryTransaction(Base, TimestampMixin):
    __tablename__ = "inventory_transactions"
    __table_args__ = (
        Index("ix_tx_facility_date", "facility_id", "transaction_date"),
        Index("ix_tx_facility_medicine_date", "facility_id", "medicine_id", "transaction_date"),
        Index("ix_tx_batch", "batch_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    facility_id: Mapped[int] = mapped_column(Integer, ForeignKey("facilities.id"), nullable=False, index=True)
    medicine_id: Mapped[int] = mapped_column(Integer, ForeignKey("medicines.id"), nullable=False, index=True)
    batch_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("batches.id"), nullable=True)
    import_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("data_imports.id"), nullable=True, index=True)
    transaction_type: Mapped[str] = mapped_column(String(50), index=True, nullable=False)  # Receipt, Issue, Adjustment_Positive, Adjustment_Negative, Transfer_In, Transfer_Out, Disposal
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    reference_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    transaction_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True
    )
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_by: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)

    facility: Mapped["Facility"] = relationship("Facility", back_populates="transactions")
    medicine: Mapped["Medicine"] = relationship("Medicine", back_populates="transactions")
    batch: Mapped[Optional["Batch"]] = relationship("Batch", back_populates="transactions")
    created_by_user: Mapped[Optional["User"]] = relationship("User", back_populates="transactions")
    data_import: Mapped[Optional["DataImport"]] = relationship("DataImport", back_populates="transactions")
