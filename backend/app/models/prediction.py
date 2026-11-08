from datetime import date, datetime, timezone
from typing import Optional, TYPE_CHECKING
from sqlalchemy import CheckConstraint, Date, DateTime, Float, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.facility import Facility
    from app.models.medicine import Medicine
    from app.models.batch import Batch


class Prediction(Base, TimestampMixin):
    __tablename__ = "predictions"
    __table_args__ = (
        CheckConstraint("risk_score >= 0.0 AND risk_score <= 1.0", name="ck_prediction_risk_score_range"),
        Index("ix_pred_facility_risk", "facility_id", "risk_type", "risk_level"),
        Index("ix_pred_medicine_risk", "medicine_id", "risk_type"),
        Index("ix_pred_date", "prediction_date"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    facility_id: Mapped[int] = mapped_column(Integer, ForeignKey("facilities.id", ondelete="CASCADE"), nullable=False, index=True)
    medicine_id: Mapped[int] = mapped_column(Integer, ForeignKey("medicines.id", ondelete="CASCADE"), nullable=False, index=True)
    batch_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("batches.id", ondelete="SET NULL"), nullable=True, index=True)
    risk_type: Mapped[str] = mapped_column(String(50), index=True, nullable=False)  # Stockout, Expiry, Overstock
    risk_score: Mapped[float] = mapped_column(Float, nullable=False)  # 0.0 - 1.0 probability
    risk_level: Mapped[str] = mapped_column(String(50), index=True, nullable=False)  # Critical, High, Medium, Low
    estimated_stockout_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    estimated_expired_units: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    estimated_financial_loss_etb: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    explanation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON-encoded SHAP or rule attributions
    prediction_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True
    )

    facility: Mapped["Facility"] = relationship("Facility", back_populates="predictions")
    medicine: Mapped["Medicine"] = relationship("Medicine", back_populates="predictions")
    batch: Mapped[Optional["Batch"]] = relationship("Batch", back_populates="predictions")
