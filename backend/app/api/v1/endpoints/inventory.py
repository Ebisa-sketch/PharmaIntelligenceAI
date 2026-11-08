from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.repositories.inventory_repository import InventoryRepository
from app.services.inventory_service import InventoryService
from app.schemas.inventory import (
    InventoryResponse,
    TransactionCreate,
    TransactionResponse,
)
from app.api.dependencies import get_current_user, check_facility_access
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[InventoryResponse])
def list_inventory(
    facility_id: Optional[int] = None,
    stock_status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if facility_id and not check_facility_access(current_user, facility_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied to requested facility")
    repo = InventoryRepository(db)
    return repo.list_by_facility(facility_id=facility_id, stock_status=stock_status, skip=skip, limit=limit)


@router.post("/transactions", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def record_transaction(
    tx_in: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not check_facility_access(current_user, tx_in.facility_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied to specified facility")
    service = InventoryService(db)
    return service.record_transaction(tx_in, user_id=current_user.id)


@router.get("/transactions", response_model=List[TransactionResponse])
def list_transactions(
    facility_id: Optional[int] = None,
    medicine_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if facility_id and not check_facility_access(current_user, facility_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied to requested facility")
    repo = InventoryRepository(db)
    return repo.list_transactions(facility_id=facility_id, medicine_id=medicine_id, skip=skip, limit=limit)
