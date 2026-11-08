from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import Boolean, CheckConstraint, Float, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.inventory import Inventory
    from app.models.batch import Batch
    from app.models.transaction import InventoryTransaction
    from app.models.forecast import Forecast
    from app.models.prediction import Prediction
    from app.models.recommendation import RedistributionRecommendation


class Medicine(Base, TimestampMixin):
    __tablename__ = "medicines"
    __table_args__ = (
        CheckConstraint("minimum_stock_level >= 0", name="ck_medicine_min_stock_non_negative"),
        CheckConstraint("reorder_point >= 0", name="ck_medicine_reorder_point_non_negative"),
        CheckConstraint("lead_time_days >= 0", name="ck_medicine_lead_time_non_negative"),
        Index("ix_medicine_category_vital", "category", "vital_classification"),
        Index("ix_medicine_code", "code", unique=True),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    brand_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    category: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    dosage_form: Mapped[str] = mapped_column(String(100), nullable=False)
    strength: Mapped[str] = mapped_column(String(100), nullable=False)
    unit_of_measure: Mapped[str] = mapped_column(String(50), nullable=False)
    is_essential: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    vital_classification: Mapped[str] = mapped_column(String(20), default="Essential", nullable=False)  # VEN classification: Vital, Essential, Non-essential
    minimum_stock_level: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    reorder_point: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    lead_time_days: Mapped[int] = mapped_column(Integer, default=30, nullable=False)

    inventories: Mapped[List["Inventory"]] = relationship("Inventory", back_populates="medicine", cascade="all, delete-orphan")
    batches: Mapped[List["Batch"]] = relationship("Batch", back_populates="medicine", cascade="all, delete-orphan")
    transactions: Mapped[List["InventoryTransaction"]] = relationship("InventoryTransaction", back_populates="medicine")
    forecasts: Mapped[List["Forecast"]] = relationship("Forecast", back_populates="medicine")
    predictions: Mapped[List["Prediction"]] = relationship("Prediction", back_populates="medicine")
    recommendations: Mapped[List["RedistributionRecommendation"]] = relationship("RedistributionRecommendation", back_populates="medicine")
