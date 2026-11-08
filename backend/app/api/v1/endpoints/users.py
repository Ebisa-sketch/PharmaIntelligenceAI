from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.api.dependencies import get_current_admin
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    repo = UserRepository(db)
    return repo.list(skip=skip, limit=limit)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    repo = UserRepository(db)
    existing = repo.get_by_email(user_in.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists.",
        )
    return repo.create(user_in)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    repo = UserRepository(db)
    user = repo.get(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
