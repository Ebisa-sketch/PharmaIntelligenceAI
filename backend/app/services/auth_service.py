from typing import Optional
from sqlalchemy.orm import Session
from app.core.security import verify_password, create_access_token
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import Token
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
        access_token = create_access_token(subject=str(user.id))
        return Token(access_token=access_token, token_type="bearer")

    def register_user(self, user_in: UserCreate) -> User:
        return self.user_repo.create(user_in)
