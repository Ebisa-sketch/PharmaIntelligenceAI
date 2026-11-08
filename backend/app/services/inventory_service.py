from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.orm import Session
from app.models.inventory import Inventory
from app.models.medicine import Medicine
from app.models.batch import Batch
from app.models.transaction import InventoryTransaction
from app.repositories.inventory_repository import InventoryRepository
from app.schemas.inventory import TransactionCreate
from app.core.exceptions import EntityNotFoundException, PharmaIntelligenceException


class InventoryService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = InventoryRepository(db)

    def record_transaction(self, tx_in: TransactionCreate, user_id: Optional[int] = None) -> InventoryTransaction:
        medicine = self.db.get(Medicine, tx_in.medicine_id)
        if not medicine:
            raise EntityNotFoundException(f"Medicine with ID {tx_in.medicine_id} not found.")

        inventory = self.repo.get_by_facility_and_medicine(tx_in.facility_id, tx_in.medicine_id)
        if not inventory:
            inventory = self.repo.create(facility_id=tx_in.facility_id, medicine_id=tx_in.medicine_id)

        # Batch adjustment if provided
        batch: Optional[Batch] = None
        if tx_in.batch_id:
            batch = self.db.get(Batch, tx_in.batch_id)
            if not batch:
                raise EntityNotFoundException(f"Batch with ID {tx_in.batch_id} not found.")

        qty = tx_in.quantity
        tx_type = tx_in.transaction_type.lower()

        if tx_type in ["receipt", "adjustment_positive", "transfer_in"]:
            inventory.current_stock += qty
            inventory.usable_stock += qty
            if batch:
                batch.quantity_remaining += qty
        elif tx_type in ["issue", "adjustment_negative", "transfer_out", "disposal"]:
            if inventory.usable_stock < qty:
                raise PharmaIntelligenceException(
                    f"Insufficient usable stock ({inventory.usable_stock}) for requested quantity ({qty})."
                )
            inventory.current_stock = max(0.0, inventory.current_stock - qty)
            inventory.usable_stock = max(0.0, inventory.usable_stock - qty)
            if batch:
                batch.quantity_remaining = max(0.0, batch.quantity_remaining - qty)
                if batch.quantity_remaining == 0:
                    batch.status = "Depleted"

        # Update months of stock and stock status
        self._update_inventory_metrics(inventory, medicine)
        inventory.last_counted_date = datetime.now(timezone.utc)

        self.db.commit()
        self.db.refresh(inventory)

        return self.repo.create_transaction(tx_in, created_by=user_id)

    def _update_inventory_metrics(self, inventory: Inventory, medicine: Medicine):
        # Calculate months of stock
        if inventory.average_monthly_consumption > 0:
            inventory.months_of_stock = round(
                inventory.usable_stock / inventory.average_monthly_consumption, 2
            )
        else:
            inventory.months_of_stock = 999.0 if inventory.usable_stock > 0 else 0.0

        # Status categorization
        if inventory.usable_stock <= 0:
            inventory.stock_status = "Stockout"
        elif inventory.usable_stock < medicine.minimum_stock_level:
            inventory.stock_status = "Understocked"
        elif inventory.usable_stock > (medicine.minimum_stock_level * 3):
            inventory.stock_status = "Overstocked"
        else:
            inventory.stock_status = "Adequate"
