from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.data_import import DataImport
    from app.models.facility import Facility
    from app.models.medicine import Medicine


class DataQualityIssue(Base, TimestampMixin):
    __tablename__ = "data_quality_issues"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    import_id: Mapped[int] = mapped_column(Integer, ForeignKey("data_imports.id"), nullable=False, index=True)
    facility_id: Mapped[int] = mapped_column(Integer, ForeignKey("facilities.id"), nullable=False, index=True)
    medicine_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("medicines.id"), nullable=True, index=True)
    issue_type: Mapped[str] = mapped_column(String(100), index=True, nullable=False)  # RECONCILIATION_ERROR, NEGATIVE_STOCK, ANOMALOUS_SPIKE, INVALID_DATE, DUPLICATE_ENTRY
    severity: Mapped[str] = mapped_column(String(20), index=True, nullable=False)  # CRITICAL, WARNING, INFO
    field_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    row_number: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON-encoded details and discrepancy metrics
    is_resolved: Mapped[bool] = mapped_column(default=False, nullable=False)

    data_import: Mapped["DataImport"] = relationship("DataImport", back_populates="quality_issues")
    facility: Mapped["Facility"] = relationship("Facility")
    medicine: Mapped[Optional["Medicine"]] = relationship("Medicine")

