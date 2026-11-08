from datetime import timedelta
from typing import Optional
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import verify_password, create_access_token
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import Token, UserSummary
from app.schemas.user import UserCreate


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = self.user_repo.get_by_email(email)
        if not user or not user.is_active:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def create_user_token(self, user: User) -> Token:
        access_token = create_access_token(
            subject=str(user.id),
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        role_name = user.role.name if user.role else "user"
        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user_id=user.id,
            role=role_name,
            facility_id=user.facility_id,
        )

    def refresh_token(self, token_str: str) -> Optional[Token]:
        try:
            payload = jwt.decode(
                token_str, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            user_id_str = payload.get("sub")
            if not user_id_str:
                return None
            user = self.user_repo.get(int(user_id_str))
            if not user or not user.is_active:
                return None
            return self.create_user_token(user)
        except JWTError:
            return None

    def get_user_summary(self, user: User) -> UserSummary:
        return UserSummary(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            role=user.role.name if user.role else "user",
            facility_id=user.facility_id,
            is_active=user.is_active,
        )

    def register_user(self, user_in: UserCreate) -> User:
        return self.user_repo.create(user_in)
