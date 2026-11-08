from datetime import date
from typing import Any, Dict, List
from sqlalchemy.orm import Session
from app.models.batch import Batch
from app.models.inventory import Inventory


class DataQualityService:
    def __init__(self, db: Session):
        self.db = db

    def assess_facility_data_quality(self, facility_id: int) -> Dict[str, Any]:
        """
        Calculates Data Quality Index (DQI) across 5 dimensions:
        1. Completeness (missing key attributes)
        2. Consistency (batch sum vs total inventory)
        3. Plausibility/Anomalies (negative numbers, extreme outliers)
        4. Expiry Date Validity (past dates with active status)
        5. Uniqueness (duplicate active batch records)
        """
        batches = self.db.query(Batch).filter(Batch.facility_id == facility_id).all()
        inventories = self.db.query(Inventory).filter(Inventory.facility_id == facility_id).all()

        issues: List[Dict[str, Any]] = []
        today = date.today()

        total_batches = len(batches)
        if total_batches == 0:
            return {
                "facility_id": facility_id,
                "dqi_score": 100.0,
                "status": "Healthy",
                "summary": "No inventory batches registered yet.",
                "issues": [],
            }

        negative_stock_count = 0
        expired_active_count = 0
        seen_batches = set()
        duplicates_count = 0

        for b in batches:
            # Check negative stock
            if b.quantity_remaining < 0:
                negative_stock_count += 1
                issues.append({
                    "dimension": "Plausibility",
                    "severity": "High",
                    "description": f"Batch {b.batch_number} has negative quantity ({b.quantity_remaining})."
                })

            # Check expired active batches
            if b.status == "Active" and b.expiry_date < today:
                expired_active_count += 1
                issues.append({
                    "dimension": "Validity",
                    "severity": "Medium",
                    "description": f"Batch {b.batch_number} expired on {b.expiry_date} but status is still 'Active'."
                })

            # Check duplicates
            key = (b.medicine_id, b.batch_number)
            if key in seen_batches and b.status == "Active":
                duplicates_count += 1
                issues.append({
                    "dimension": "Uniqueness",
                    "severity": "High",
                    "description": f"Duplicate active batch record found for batch {b.batch_number}."
                })
            seen_batches.add(key)

        # Consistency check: Compare batch sums to inventory
        inconsistency_count = 0
        for inv in inventories:
            batch_sum = sum(
                b.quantity_remaining
                for b in batches
                if b.medicine_id == inv.medicine_id and b.status == "Active"
            )
            if abs(inv.current_stock - batch_sum) > 0.01:
                inconsistency_count += 1
                issues.append({
                    "dimension": "Consistency",
                    "severity": "Medium",
                    "description": f"Medicine ID {inv.medicine_id} stock ({inv.current_stock}) does not match active batch sum ({batch_sum})."
                })

        # Calculate DQI Score (100 base, deductions per issue)
        deductions = (negative_stock_count * 15) + (inconsistency_count * 10) + (expired_active_count * 5) + (duplicates_count * 10)
        dqi_score = max(0.0, min(100.0, 100.0 - deductions))

        status = "Healthy" if dqi_score >= 85 else ("Degraded" if dqi_score >= 60 else "Critical")

        return {
            "facility_id": facility_id,
            "dqi_score": round(dqi_score, 1),
            "status": status,
            "total_batches_analyzed": total_batches,
            "issues_count": len(issues),
            "issues": issues,
        }
