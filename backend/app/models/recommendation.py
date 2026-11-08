from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.facility import Facility
    from app.models.medicine import Medicine
    from app.models.batch import Batch
    from app.models.user import User


class RedistributionRecommendation(Base, TimestampMixin):
    __tablename__ = "redistribution_recommendations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    source_facility_id: Mapped[int] = mapped_column(Integer, ForeignKey("facilities.id"), nullable=False)
    target_facility_id: Mapped[int] = mapped_column(Integer, ForeignKey("facilities.id"), nullable=False)
    medicine_id: Mapped[int] = mapped_column(Integer, ForeignKey("medicines.id"), nullable=False)
    batch_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("batches.id"), nullable=True)
    quantity_recommended: Mapped[float] = mapped_column(Float, nullable=False)
    transport_distance_km: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    estimated_transfer_cost_etb: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    prevented_wastage_cost_etb: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="Pending", index=True, nullable=False)  # Pending, Approved, Rejected, In_Transit, Completed
    priority: Mapped[str] = mapped_column(String(50), default="Medium", nullable=False)  # High, Medium, Low
    rationale: Mapped[str] = mapped_column(Text, nullable=False)
    reviewed_by: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
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
