from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.medicine import Medicine
from app.models.batch import Batch
from app.schemas.medicine import MedicineCreate, MedicineUpdate, BatchCreate


class MedicineRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, medicine_id: int) -> Optional[Medicine]:
        return self.db.get(Medicine, medicine_id)

    def get_by_code(self, code: str) -> Optional[Medicine]:
        stmt = select(Medicine).where(Medicine.code == code)
        return self.db.scalars(stmt).first()

    def list(
        self,
        category: Optional[str] = None,
        is_essential: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Medicine]:
        stmt = select(Medicine)
        if category:
            stmt = stmt.where(Medicine.category == category)
        if is_essential is not None:
            stmt = stmt.where(Medicine.is_essential == is_essential)
        stmt = stmt.offset(skip).limit(limit)
        return list(self.db.scalars(stmt).all())

    def create(self, medicine_in: MedicineCreate) -> Medicine:
        db_medicine = Medicine(**medicine_in.model_dump())
        self.db.add(db_medicine)
        self.db.commit()
        self.db.refresh(db_medicine)
        return db_medicine

    def update(self, db_medicine: Medicine, medicine_in: MedicineUpdate) -> Medicine:
        update_data = medicine_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_medicine, field, value)
        self.db.commit()
        self.db.refresh(db_medicine)
        return db_medicine

    def get_batch(self, batch_id: int) -> Optional[Batch]:
        return self.db.get(Batch, batch_id)

    def get_batches(
        self,
        medicine_id: Optional[int] = None,
        facility_id: Optional[int] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Batch]:
        stmt = select(Batch)
        if medicine_id:
            stmt = stmt.where(Batch.medicine_id == medicine_id)
        if facility_id:
            stmt = stmt.where(Batch.facility_id == facility_id)
        if status:
            stmt = stmt.where(Batch.status == status)
        stmt = stmt.offset(skip).limit(limit)
        return list(self.db.scalars(stmt).all())

    def create_batch(self, batch_in: BatchCreate) -> Batch:
        db_batch = Batch(**batch_in.model_dump())
        self.db.add(db_batch)
        self.db.commit()
        self.db.refresh(db_batch)
        return db_batch
