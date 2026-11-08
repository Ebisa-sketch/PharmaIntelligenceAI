from datetime import datetime, timezone
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.facility import Facility
    from app.models.user import User
    from app.models.data_quality import DataQualityIssue
    from app.models.transaction import InventoryTransaction


class DataImport(Base, TimestampMixin):
    __tablename__ = "data_imports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    facility_id: Mapped[int] = mapped_column(Integer, ForeignKey("facilities.id"), nullable=False, index=True)
    uploaded_by_user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_hash_sha256: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    total_rows: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    valid_rows: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    rejected_rows: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    dq_score: Mapped[float] = mapped_column(Float, default=100.0, nullable=False)  # 0.0 - 100.0%
    status: Mapped[str] = mapped_column(String(50), default="COMPLETED", nullable=False)  # PENDING, PROCESSING, COMPLETED, FAILED

    facility: Mapped["Facility"] = relationship("Facility", backref="imports")
    uploaded_by: Mapped["User"] = relationship("User", backref="data_imports")
    quality_issues: Mapped[List["DataQualityIssue"]] = relationship("DataQualityIssue", back_populates="data_import", cascade="all, delete-orphan")
    transactions: Mapped[List["InventoryTransaction"]] = relationship("InventoryTransaction", back_populates="data_import")

