from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.role import Role
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, user_id: int) -> Optional[User]:
        return self.db.get(User, user_id)

    def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        return self.db.scalars(stmt).first()

    def list(self, skip: int = 0, limit: int = 100) -> List[User]:
        stmt = select(User).offset(skip).limit(limit)
        return list(self.db.scalars(stmt).all())

    def create(self, user_in: UserCreate) -> User:
        db_user = User(
            email=user_in.email,
            hashed_password=get_password_hash(user_in.password),
            full_name=user_in.full_name,
            role_id=user_in.role_id,
            facility_id=user_in.facility_id,
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update(self, db_user: User, user_in: UserUpdate) -> User:
        update_data = user_in.model_dump(exclude_unset=True)
        if "password" in update_data and update_data["password"]:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        for field, value in update_data.items():
            setattr(db_user, field, value)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_role_by_name(self, name: str) -> Optional[Role]:
        stmt = select(Role).where(Role.name == name)
        return self.db.scalars(stmt).first()
