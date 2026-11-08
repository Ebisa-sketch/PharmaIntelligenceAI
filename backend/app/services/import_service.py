import csv
import io
from datetime import datetime
from typing import Any, Dict, List
from sqlalchemy.orm import Session
from app.models.facility import Facility
from app.models.medicine import Medicine
from app.models.batch import Batch
from app.models.inventory import Inventory
from app.core.exceptions import DataQualityValidationError


class ImportService:
    def __init__(self, db: Session):
        self.db = db

    def parse_and_import_csv(self, file_content: str, facility_id: int) -> Dict[str, Any]:
        """
        Parses CSV data containing columns:
        medicine_code,batch_number,expiry_date,quantity,unit_cost_etb
        """
        reader = csv.DictReader(io.StringIO(file_content))
        imported_rows = 0
        errors: List[str] = []

        facility = self.db.get(Facility, facility_id)
        if not facility:
            raise DataQualityValidationError(f"Target facility ID {facility_id} does not exist.")

        for row_idx, row in enumerate(reader, start=1):
            try:
                med_code = row.get("medicine_code", "").strip()
                batch_no = row.get("batch_number", "").strip()
                expiry_str = row.get("expiry_date", "").strip()
                quantity = float(row.get("quantity", 0))
                cost = float(row.get("unit_cost_etb", 0.0))

                if not med_code or not batch_no or not expiry_str:
                    errors.append(f"Row {row_idx}: Missing required fields (code/batch/expiry).")
                    continue

                expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d").date()

                medicine = self.db.query(Medicine).filter(Medicine.code == med_code).first()
                if not medicine:
                    errors.append(f"Row {row_idx}: Unknown medicine code '{med_code}'.")
                    continue

                batch = Batch(
                    facility_id=facility.id,
                    medicine_id=medicine.id,
                    batch_number=batch_no,
                    expiry_date=expiry_date,
                    quantity_initial=quantity,
                    quantity_remaining=quantity,
                    unit_cost_etb=cost,
                    status="Active",
                )
                self.db.add(batch)

                # Sync Inventory
                inventory = self.db.query(Inventory).filter(
                    Inventory.facility_id == facility.id,
                    Inventory.medicine_id == medicine.id
                ).first()

                if not inventory:
                    inventory = Inventory(
                        facility_id=facility.id,
                        medicine_id=medicine.id,
                        current_stock=quantity,
                        usable_stock=quantity,
                    )
                    self.db.add(inventory)
                else:
                    inventory.current_stock += quantity
                    inventory.usable_stock += quantity

                imported_rows += 1
            except Exception as e:
                errors.append(f"Row {row_idx}: {str(e)}")

        self.db.commit()
        return {
            "facility_id": facility_id,
            "imported_count": imported_rows,
            "errors": errors,
            "status": "success" if not errors else "partial_success",
        }
