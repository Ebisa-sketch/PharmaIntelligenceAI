from datetime import date
from typing import List
from sqlalchemy.orm import Session
from app.models.batch import Batch
from app.models.medicine import Medicine
from app.models.facility import Facility
from app.models.inventory import Inventory
from app.schemas.forecasting import ExpiryRiskResponse


class ExpiryService:
    def __init__(self, db: Session):
        self.db = db

    def evaluate_expiry_risks(self, facility_id: int) -> List[ExpiryRiskResponse]:
        """
        Assesses expiry risk on active batches using First-Expiry-First-Out (FEFO) simulation.
        Compares projected consumption before expiry against quantity in batch.
        """
        facility = self.db.get(Facility, facility_id)
        if not facility:
            return []

        batches = self.db.query(Batch).filter(
            Batch.facility_id == facility_id,
            Batch.status == "Active",
            Batch.quantity_remaining > 0
        ).order_by(Batch.expiry_date.asc()).all()

        results: List[ExpiryRiskResponse] = []
        today = date.today()

        for b in batches:
            medicine = self.db.get(Medicine, b.medicine_id)
            if not medicine:
                continue

            inv = self.db.query(Inventory).filter(
                Inventory.facility_id == facility_id,
                Inventory.medicine_id == medicine.id
            ).first()

            monthly_rate = inv.average_monthly_consumption if (inv and inv.average_monthly_consumption > 0) else 15.0
            daily_rate = monthly_rate / 30.0

            days_to_expiry = (b.expiry_date - today).days

            if days_to_expiry <= 0:
                # Already expired
                qty_at_risk = b.quantity_remaining
                risk_level = "Critical"
                action = "Batch has reached or passed expiry. Quarantine immediately for safe disposal."
            else:
                expected_consumption_before_expiry = days_to_expiry * daily_rate
                surplus = b.quantity_remaining - expected_consumption_before_expiry

                if surplus > 0:
                    qty_at_risk = round(surplus, 1)
                    if days_to_expiry < 90:
                        risk_level = "High"
                        action = "Redistribute surplus to neighboring high-volume facilities or prioritize under FEFO."
                    elif days_to_expiry < 180:
                        risk_level = "Medium"
                        action = "Monitor consumption closely; flag for potential inter-facility transfer."
                    else:
                        risk_level = "Low"
                        action = "Projected consumption slightly exceeds standard buffer. Review dispensing rates."
                else:
                    qty_at_risk = 0.0
                    risk_level = "Low"
                    action = "Stock expected to be fully utilized before expiry date."

            estimated_loss = round(qty_at_risk * b.unit_cost_etb, 2)

            if risk_level in ["Critical", "High", "Medium"]:
                results.append(
                    ExpiryRiskResponse(
                        facility_id=facility.id,
                        facility_name=facility.name,
                        medicine_id=medicine.id,
                        medicine_name=medicine.name,
                        batch_id=b.id,
                        batch_number=b.batch_number,
                        expiry_date=b.expiry_date,
                        quantity_at_risk=qty_at_risk,
                        estimated_loss_etb=estimated_loss,
                        risk_level=risk_level,
                        monthly_consumption_rate=round(monthly_rate, 1),
                        recommended_action=action,
                    )
                )

        results.sort(key=lambda r: (r.risk_level == "Critical", r.estimated_loss_etb), reverse=True)
        return results
