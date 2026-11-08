"""
FEFO Expiry Risk Simulation Engine for PharmaIntelligence AI

Implements mathematical queue depletion under First-Expired-First-Out (FEFO):
- Sorts batches ascending by expiration date: T_1 <= T_2 <= ... <= T_K
- Computes cumulative demand expected up to expiration: D_k = sum_{t=1}^{T_k} d(t)
- Computes cumulative stock queue: S_k = sum_{i=1}^k Q_i
- Calculates Projected Unused Stock at Expiry: PUSE_k = max(0, min(Q_k, S_k - D_k))
- Calculates Financial Value at Risk (FVR_k = PUSE_k * Unit Cost ETB)

Reference: docs/06-ai-documentation/expiry-risk-methodology.md
"""

from datetime import date
from typing import Any, Dict, List, Optional


class FEFOExpirySimulator:
    def __init__(self, critical_days_threshold: int = 90, warning_days_threshold: int = 180):
        self.critical_days = critical_days_threshold
        self.warning_days = warning_days_threshold

    def simulate_batches(
        self,
        facility_id: int,
        facility_name: str,
        medicine_id: int,
        medicine_name: str,
        batches: List[Dict[str, Any]],
        daily_consumption_rate: float,
        today: Optional[date] = None,
    ) -> List[Dict[str, Any]]:
        """
        Simulates multi-batch FEFO depletion for a specific medicine at a facility.
        batches should be dicts with keys:
        id, batch_number, expiry_date, quantity_remaining, unit_cost_etb, status
        """
        current_date = today or date.today()
        daily_rate = max(0.001, daily_consumption_rate)

        # Filter active batches with remaining quantity
        active_batches = [
            b for b in batches
            if b.get("status", "Active") == "Active" and b.get("quantity_remaining", 0) > 0
        ]

        # Sort ascending by expiration date (strict FEFO priority)
        active_batches.sort(key=lambda b: b["expiry_date"])

        results: List[Dict[str, Any]] = []
        cumulative_stock = 0.0

        for b in active_batches:
            batch_id = b.get("id")
            batch_no = b.get("batch_number", "UNKNOWN")
            exp_date = b["expiry_date"]
            if isinstance(exp_date, str):
                exp_date = date.fromisoformat(exp_date)

            qty = float(b.get("quantity_remaining", 0.0))
            unit_cost = float(b.get("unit_cost_etb", 0.0))

            cumulative_stock += qty
            days_to_expiry = (exp_date - current_date).days

            if days_to_expiry <= 0:
                # Already expired
                puse = qty
                risk_level = "Critical"
                action = "Expired lot. Quarantine immediately from dispensing shelves for formal destruction."
            else:
                # Cumulative expected demand up to this batch's expiration date
                cumulative_demand_at_expiry = days_to_expiry * daily_rate

                # PUSE formulation: max(0, min(Q_k, S_k - D_k))
                surplus = cumulative_stock - cumulative_demand_at_expiry
                puse = max(0.0, min(qty, surplus))

                if puse > 0:
                    if days_to_expiry < self.critical_days:
                        risk_level = "Critical"
                        action = "High waste risk. Issue immediate lateral redistribution transfer or prioritize for rapid dispensing."
                    elif days_to_expiry < self.warning_days:
                        risk_level = "High"
                        action = "Surplus at risk. Flag for regional redistribution or pause upcoming supplier receipts."
                    else:
                        risk_level = "Medium"
                        action = "Moderate surplus projected. Monitor local consumption trends."
                else:
                    risk_level = "Low"
                    action = "Batch expected to be fully absorbed prior to expiration under FEFO priority."

            fvr = round(puse * unit_cost, 2)
            monthly_rate = round(daily_rate * 30.0, 1)

            results.append({
                "facility_id": facility_id,
                "facility_name": facility_name,
                "medicine_id": medicine_id,
                "medicine_name": medicine_name,
                "batch_id": batch_id,
                "batch_number": batch_no,
                "expiry_date": exp_date,
                "quantity_remaining": round(qty, 2),
                "days_until_expiry": days_to_expiry,
                "quantity_at_risk": round(puse, 2),
                "estimated_loss_etb": fvr,
                "risk_level": risk_level,
                "monthly_consumption_rate": monthly_rate,
                "recommended_action": action,
            })

        # Sort results: Critical first, then by monetary loss
        results.sort(key=lambda r: (r["risk_level"] == "Critical", r["estimated_loss_etb"]), reverse=True)
        return results

