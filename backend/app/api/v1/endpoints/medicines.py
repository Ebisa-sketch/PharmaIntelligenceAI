from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.repositories.medicine_repository import MedicineRepository
from app.schemas.medicine import MedicineCreate, MedicineResponse, MedicineUpdate
from app.api.dependencies import get_current_user, get_current_admin
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[MedicineResponse])
def list_medicines(
    category: Optional[str] = None,
    is_essential: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = MedicineRepository(db)
    return repo.list(category=category, is_essential=is_essential, skip=skip, limit=limit)


@router.post("/", response_model=MedicineResponse, status_code=status.HTTP_201_CREATED)
def create_medicine(
    med_in: MedicineCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    repo = MedicineRepository(db)
    existing = repo.get_by_code(med_in.code)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Medicine code '{med_in.code}' already exists.",
        )
    return repo.create(med_in)


@router.get("/{medicine_id}", response_model=MedicineResponse)
def get_medicine(
    medicine_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = MedicineRepository(db)
    med = repo.get(medicine_id)
    if not med:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medicine not found")
    return med
