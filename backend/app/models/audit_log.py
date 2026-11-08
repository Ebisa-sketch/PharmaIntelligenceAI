from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User


class AuditLog(Base, TimestampMixin):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    action: Mapped[str] = mapped_column(String(100), index=True, nullable=False)  # USER_LOGIN, INVENTORY_ADJUST, REDISTRIBUTION_APPROVE, etc.
    entity_type: Mapped[str] = mapped_column(String(100), index=True, nullable=False)  # User, Inventory, Batch, Recommendation, etc.
    entity_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON or structured description
    ip_address: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True
    )

    user: Mapped[Optional["User"]] = relationship("User", back_populates="audit_logs")
