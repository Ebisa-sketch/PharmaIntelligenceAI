import json
from datetime import date, datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

from app.models.batch import Batch
from app.models.medicine import Medicine
from app.models.facility import Facility
from app.models.inventory import Inventory
from app.models.prediction import Prediction
from app.schemas.forecasting import ExpiryRiskResponse
from app.ml.expiry_simulator import FEFOExpirySimulator
from app.ml.explainability import ExplainabilityEngine
from app.core.exceptions import EntityNotFoundException


class ExpiryService:
    def __init__(self, db: Session):
        self.db = db
        self.simulator = FEFOExpirySimulator()

    def evaluate_expiry_risks(
        self, facility_id: int, persist: bool = True
    ) -> List[ExpiryRiskResponse]:
        """
        Assesses expiry risk on active batches using First-Expired-First-Out (FEFO) simulation.
        Computes Projected Unused Stock at Expiry (PUSE) and Financial Value at Risk (FVR in ETB).
        Generates XAI diagnostic summaries and optionally persists to `predictions` table.
        """
        facility = self.db.get(Facility, facility_id)
        if not facility:
            raise EntityNotFoundException(f"Facility ID {facility_id} not found.")

        # Group active batches by medicine_id
        batches = (
            self.db.query(Batch)
            .filter(
                Batch.facility_id == facility_id,
                Batch.status == "Active",
                Batch.quantity_remaining > 0,
            )
            .order_by(Batch.expiry_date.asc())
            .all()
        )

        batches_by_med: Dict[int, List[Batch]] = {}
        for b in batches:
            batches_by_med.setdefault(b.medicine_id, []).append(b)

        results: List[ExpiryRiskResponse] = []
        predictions_to_persist = []

        for med_id, med_batches in batches_by_med.items():
            medicine = self.db.get(Medicine, med_id)
            if not medicine:
                continue

            inv = (
                self.db.query(Inventory)
                .filter(
                    Inventory.facility_id == facility_id,
                    Inventory.medicine_id == med_id,
                )
                .first()
            )
            monthly_rate = inv.average_monthly_consumption if (inv and inv.average_monthly_consumption > 0) else 15.0
            daily_rate = monthly_rate / 30.0

            # Convert ORM batches to dict format for simulation
            batch_dicts = [
                {
                    "id": b.id,
                    "batch_number": b.batch_number,
                    "expiry_date": b.expiry_date,
                    "quantity_remaining": b.quantity_remaining,
                    "unit_cost_etb": b.unit_cost_etb,
                    "status": b.status,
                }
                for b in med_batches
            ]

            # Run FEFO queue simulation
            sim_results = self.simulator.simulate_batches(
                facility_id=facility.id,
                facility_name=facility.name,
                medicine_id=medicine.id,
                medicine_name=medicine.name,
                batches=batch_dicts,
                daily_consumption_rate=daily_rate,
            )

            for sim_item in sim_results:
                # Explainability
                xai = ExplainabilityEngine.explain_expiry_risk(
                    facility_name=facility.name,
                    medicine_name=medicine.name,
                    batch_number=sim_item["batch_number"],
                    expiry_data=sim_item,
                )

                response_item = ExpiryRiskResponse(
                    facility_id=facility.id,
                    facility_name=facility.name,
                    medicine_id=medicine.id,
                    medicine_name=medicine.name,
                    batch_id=sim_item["batch_id"],
                    batch_number=sim_item["batch_number"],
                    expiry_date=sim_item["expiry_date"],
                    quantity_at_risk=sim_item["quantity_at_risk"],
                    estimated_loss_etb=sim_item["estimated_loss_etb"],
                    risk_level=sim_item["risk_level"],
                    monthly_consumption_rate=sim_item["monthly_consumption_rate"],
                    recommended_action=sim_item["recommended_action"],
                    explanation=xai["plain_language_summary"],
                )
                results.append(response_item)

                if persist and sim_item["risk_level"] in ["Critical", "High", "Medium"]:
                    pred = Prediction(
                        facility_id=facility.id,
                        medicine_id=medicine.id,
                        batch_id=sim_item["batch_id"],
                        risk_type="Expiry",
                        risk_score=1.0 if sim_item["risk_level"] == "Critical" else (0.75 if sim_item["risk_level"] == "High" else 0.40),
                        risk_level=sim_item["risk_level"],
                        estimated_expired_units=sim_item["quantity_at_risk"],
                        estimated_financial_loss_etb=sim_item["estimated_loss_etb"],
                        explanation=json.dumps({
                            "summary": xai["plain_language_summary"],
                            "formula": xai["formula_applied"],
                            "days_remaining": sim_item["days_until_expiry"],
                        }),
                        prediction_date=datetime.now(timezone.utc),
                    )
                    predictions_to_persist.append(pred)

        if persist and predictions_to_persist:
            self.db.add_all(predictions_to_persist)
            self.db.commit()

        # Sort: Critical first, then highest monetary loss
        results.sort(key=lambda r: (r.risk_level == "Critical", r.estimated_loss_etb), reverse=True)
        return results
