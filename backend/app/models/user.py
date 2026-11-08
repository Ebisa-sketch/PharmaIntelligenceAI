from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.role import Role
    from app.models.facility import Facility
    from app.models.transaction import InventoryTransaction
    from app.models.audit_log import AuditLog
    from app.models.recommendation import RedistributionRecommendation


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("roles.id"), nullable=False)
    facility_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("facilities.id"), nullable=True)

    role: Mapped["Role"] = relationship("Role", back_populates="users")
    facility: Mapped[Optional["Facility"]] = relationship("Facility", back_populates="users")
    transactions: Mapped[List["InventoryTransaction"]] = relationship("InventoryTransaction", back_populates="created_by_user")
    audit_logs: Mapped[List["AuditLog"]] = relationship("AuditLog", back_populates="user")
    reviewed_recommendations: Mapped[List["RedistributionRecommendation"]] = relationship("RedistributionRecommendation", back_populates="reviewer")
