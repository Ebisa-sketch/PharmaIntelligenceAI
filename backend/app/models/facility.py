from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import Boolean, CheckConstraint, Float, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.inventory import Inventory
    from app.models.batch import Batch
    from app.models.transaction import InventoryTransaction
    from app.models.forecast import Forecast
    from app.models.prediction import Prediction
    from app.models.recommendation import RedistributionRecommendation


class Facility(Base, TimestampMixin):
    __tablename__ = "facilities"
    __table_args__ = (
        CheckConstraint("storage_capacity_m3 IS NULL OR storage_capacity_m3 >= 0", name="ck_facility_storage_capacity"),
        Index("ix_facility_region_type", "region", "facility_type"),
        Index("ix_facility_code", "code", unique=True),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), index=True, nullable=False)
    facility_type: Mapped[str] = mapped_column(String(100), nullable=False)  # e.g., Specialized Hospital, Health Center
    region: Mapped[str] = mapped_column(String(100), index=True, nullable=False)  # e.g., Addis Ababa, Oromia, Amhara
    zone: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    woreda: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    storage_capacity_m3: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    users: Mapped[List["User"]] = relationship("User", back_populates="facility")
    inventories: Mapped[List["Inventory"]] = relationship("Inventory", back_populates="facility", cascade="all, delete-orphan")
    batches: Mapped[List["Batch"]] = relationship("Batch", back_populates="facility", cascade="all, delete-orphan")
    transactions: Mapped[List["InventoryTransaction"]] = relationship("InventoryTransaction", back_populates="facility")
    forecasts: Mapped[List["Forecast"]] = relationship("Forecast", back_populates="facility")
    predictions: Mapped[List["Prediction"]] = relationship("Prediction", back_populates="facility")
    outgoing_recommendations: Mapped[List["RedistributionRecommendation"]] = relationship(
        "RedistributionRecommendation",
        foreign_keys="RedistributionRecommendation.source_facility_id",
        back_populates="source_facility"
    )
    incoming_recommendations: Mapped[List["RedistributionRecommendation"]] = relationship(
        "RedistributionRecommendation",
        foreign_keys="RedistributionRecommendation.target_facility_id",
        back_populates="target_facility"
    )
