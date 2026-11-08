from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.repositories.medicine_repository import MedicineRepository
from app.schemas.medicine import BatchCreate, BatchResponse
from app.api.dependencies import get_current_user, check_facility_access
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[BatchResponse])
def list_batches(
    facility_id: Optional[int] = None,
    medicine_id: Optional[int] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if facility_id and not check_facility_access(current_user, facility_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied to requested facility")
    repo = MedicineRepository(db)
    return repo.get_batches(facility_id=facility_id, medicine_id=medicine_id, status=status, skip=skip, limit=limit)


@router.post("/", response_model=BatchResponse, status_code=status.HTTP_201_CREATED)
def create_batch(
    batch_in: BatchCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not check_facility_access(current_user, batch_in.facility_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied to specified facility")
    repo = MedicineRepository(db)
    return repo.create_batch(batch_in)


@router.get("/{batch_id}", response_model=BatchResponse)
def get_batch(
    batch_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = MedicineRepository(db)
    batch = repo.get_batch(batch_id)
    if not batch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Batch not found")
    if not check_facility_access(current_user, batch.facility_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return batch
