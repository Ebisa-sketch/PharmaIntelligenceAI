from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import CheckConstraint, DateTime, Float, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.facility import Facility
    from app.models.medicine import Medicine
    from app.models.batch import Batch
    from app.models.user import User


class RedistributionRecommendation(Base, TimestampMixin):
    __tablename__ = "redistribution_recommendations"
    __table_args__ = (
        CheckConstraint("quantity_recommended > 0", name="ck_rec_quantity_positive"),
        CheckConstraint("source_facility_id != target_facility_id", name="ck_rec_distinct_facilities"),
        Index("ix_rec_facilities_status", "source_facility_id", "target_facility_id", "status"),
        Index("ix_rec_status_priority", "status", "priority"),
        Index("ix_rec_medicine", "medicine_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    source_facility_id: Mapped[int] = mapped_column(Integer, ForeignKey("facilities.id"), nullable=False, index=True)
    target_facility_id: Mapped[int] = mapped_column(Integer, ForeignKey("facilities.id"), nullable=False, index=True)
    medicine_id: Mapped[int] = mapped_column(Integer, ForeignKey("medicines.id"), nullable=False, index=True)
    batch_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("batches.id"), nullable=True, index=True)
    quantity_recommended: Mapped[float] = mapped_column(Float, nullable=False)
    transport_distance_km: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    estimated_transfer_cost_etb: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    prevented_wastage_cost_etb: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="Pending", index=True, nullable=False)  # Pending, Approved, Rejected, In_Transit, Completed
    priority: Mapped[str] = mapped_column(String(50), default="Medium", nullable=False, index=True)  # High, Medium, Low
    rationale: Mapped[str] = mapped_column(Text, nullable=False)
    reviewed_by: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    reviewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    source_facility: Mapped["Facility"] = relationship(
        "Facility",
        foreign_keys=[source_facility_id],
        back_populates="outgoing_recommendations"
    )
    target_facility: Mapped["Facility"] = relationship(
        "Facility",
        foreign_keys=[target_facility_id],
        back_populates="incoming_recommendations"
    )
    medicine: Mapped["Medicine"] = relationship("Medicine", back_populates="recommendations")
    batch: Mapped[Optional["Batch"]] = relationship("Batch", back_populates="recommendations")
    reviewer: Mapped[Optional["User"]] = relationship("User", back_populates="reviewed_recommendations")
