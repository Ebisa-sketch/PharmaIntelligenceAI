from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.repositories.facility_repository import FacilityRepository
from app.schemas.facility import FacilityCreate, FacilityResponse, FacilityUpdate
from app.api.dependencies import get_current_user, get_current_admin
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[FacilityResponse])
def list_facilities(
    region: Optional[str] = None,
    facility_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = FacilityRepository(db)
    return repo.list(region=region, facility_type=facility_type, skip=skip, limit=limit)


@router.post("/", response_model=FacilityResponse, status_code=status.HTTP_201_CREATED)
def create_facility(
    facility_in: FacilityCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    repo = FacilityRepository(db)
    existing = repo.get_by_code(facility_in.code)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Facility code '{facility_in.code}' already registered.",
        )
    return repo.create(facility_in)


@router.get("/{facility_id}", response_model=FacilityResponse)
def get_facility(
    facility_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = FacilityRepository(db)
    facility = repo.get(facility_id)
    if not facility:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Facility not found")
    return facility
