from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.inventory import Inventory
from app.models.transaction import InventoryTransaction
from app.schemas.inventory import TransactionCreate


class InventoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, inventory_id: int) -> Optional[Inventory]:
        return self.db.get(Inventory, inventory_id)

    def get_by_facility_and_medicine(self, facility_id: int, medicine_id: int) -> Optional[Inventory]:
        stmt = select(Inventory).where(
            Inventory.facility_id == facility_id,
            Inventory.medicine_id == medicine_id
        )
        return self.db.scalars(stmt).first()

    def list_by_facility(
        self,
        facility_id: Optional[int] = None,
        stock_status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Inventory]:
        stmt = select(Inventory)
        if facility_id:
            stmt = stmt.where(Inventory.facility_id == facility_id)
        if stock_status:
            stmt = stmt.where(Inventory.stock_status == stock_status)
        stmt = stmt.offset(skip).limit(limit)
        return list(self.db.scalars(stmt).all())

    def create(self, facility_id: int, medicine_id: int, current_stock: float = 0.0) -> Inventory:
        inventory = Inventory(
            facility_id=facility_id,
            medicine_id=medicine_id,
            current_stock=current_stock,
            usable_stock=current_stock,
        )
        self.db.add(inventory)
        self.db.commit()
        self.db.refresh(inventory)
        return inventory

    def update(self, db_inventory: Inventory, update_data: dict) -> Inventory:
        for field, value in update_data.items():
            setattr(db_inventory, field, value)
        self.db.commit()
        self.db.refresh(db_inventory)
        return db_inventory

    def create_transaction(self, tx_in: TransactionCreate, created_by: Optional[int] = None) -> InventoryTransaction:
        db_tx = InventoryTransaction(
            facility_id=tx_in.facility_id,
            medicine_id=tx_in.medicine_id,
            batch_id=tx_in.batch_id,
            transaction_type=tx_in.transaction_type,
            quantity=tx_in.quantity,
            reference_number=tx_in.reference_number,
            notes=tx_in.notes,
            created_by=created_by,
        )
        self.db.add(db_tx)
        self.db.commit()
        self.db.refresh(db_tx)
        return db_tx

    def list_transactions(
        self,
        facility_id: Optional[int] = None,
        medicine_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[InventoryTransaction]:
        stmt = select(InventoryTransaction)
        if facility_id:
            stmt = stmt.where(InventoryTransaction.facility_id == facility_id)
        if medicine_id:
            stmt = stmt.where(InventoryTransaction.medicine_id == medicine_id)
        stmt = stmt.order_by(InventoryTransaction.transaction_date.desc()).offset(skip).limit(limit)
        return list(self.db.scalars(stmt).all())
