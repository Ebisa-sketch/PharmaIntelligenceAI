from typing import List, TYPE_CHECKING
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User


class Role(Base, TimestampMixin):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    users: Mapped[List["User"]] = relationship("User", back_populates="role")
