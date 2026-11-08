from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.facility import Facility
from app.schemas.facility import FacilityCreate, FacilityUpdate


class FacilityRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, facility_id: int) -> Optional[Facility]:
        return self.db.get(Facility, facility_id)

    def get_by_code(self, code: str) -> Optional[Facility]:
        stmt = select(Facility).where(Facility.code == code)
        return self.db.scalars(stmt).first()

    def list(
        self,
        region: Optional[str] = None,
        facility_type: Optional[str] = None,
        is_active: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Facility]:
        stmt = select(Facility)
        if region:
            stmt = stmt.where(Facility.region == region)
        if facility_type:
            stmt = stmt.where(Facility.facility_type == facility_type)
        if is_active is not None:
            stmt = stmt.where(Facility.is_active == is_active)
        stmt = stmt.offset(skip).limit(limit)
        return list(self.db.scalars(stmt).all())

    def create(self, facility_in: FacilityCreate) -> Facility:
        db_facility = Facility(**facility_in.model_dump())
        self.db.add(db_facility)
        self.db.commit()
        self.db.refresh(db_facility)
        return db_facility

    def update(self, db_facility: Facility, facility_in: FacilityUpdate) -> Facility:
        update_data = facility_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_facility, field, value)
        self.db.commit()
        self.db.refresh(db_facility)
        return db_facility
