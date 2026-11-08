from datetime import date
from typing import Optional, TYPE_CHECKING
from sqlalchemy import Date, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.facility import Facility
    from app.models.medicine import Medicine


class Forecast(Base, TimestampMixin):
    __tablename__ = "forecasts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    facility_id: Mapped[int] = mapped_column(Integer, ForeignKey("facilities.id"), nullable=False)
    medicine_id: Mapped[int] = mapped_column(Integer, ForeignKey("medicines.id"), nullable=False)
    model_type: Mapped[str] = mapped_column(String(100), nullable=False)  # Ensemble, LightGBM, SARIMAX, Prophet
    forecast_date: Mapped[date] = mapped_column(Date, nullable=False)
    target_period_start: Mapped[date] = mapped_column(Date, nullable=False)
    target_period_end: Mapped[date] = mapped_column(Date, nullable=False)
    forecast_value: Mapped[float] = mapped_column(Float, nullable=False)
    confidence_interval_lower: Mapped[float] = mapped_column(Float, nullable=False)
    confidence_interval_upper: Mapped[float] = mapped_column(Float, nullable=False)
    mape_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    uncertainty_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    features_used: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON-encoded metadata

    facility: Mapped["Facility"] = relationship("Facility", back_populates="forecasts")
    medicine: Mapped["Medicine"] = relationship("Medicine", back_populates="forecasts")
