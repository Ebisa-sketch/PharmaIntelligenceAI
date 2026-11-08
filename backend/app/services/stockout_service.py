from datetime import date, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.inventory import Inventory
from app.models.medicine import Medicine
from app.models.facility import Facility
from app.schemas.forecasting import StockoutRiskResponse


class StockoutService:
    def __init__(self, db: Session):
        self.db = db

    def evaluate_facility_stockouts(self, facility_id: int) -> List[StockoutRiskResponse]:
        """
        Evaluates stockout risks across all medicines in a facility.
        Calculates:
        - Days until stockout = Usable Stock / Daily Consumption
        - Compares against supplier lead time (lead_time_days)
        """
        facility = self.db.get(Facility, facility_id)
        if not facility:
            return []

        inventories = self.db.query(Inventory).filter(Inventory.facility_id == facility_id).all()
        results: List[StockoutRiskResponse] = []

        for inv in inventories:
            medicine = self.db.get(Medicine, inv.medicine_id)
            if not medicine:
                continue

            daily_consumption = (inv.average_monthly_consumption / 30.0) if inv.average_monthly_consumption > 0 else 2.0
            usable_stock = max(0.0, inv.usable_stock)

            days_remaining = usable_stock / daily_consumption if daily_consumption > 0 else 999.0
            lead_time = float(medicine.lead_time_days)

            # Determine risk
            if days_remaining <= 0:
                risk_score = 1.0
                risk_level = "Critical"
                action = "Emergency replenishment order or immediate inter-facility transfer required."
            elif days_remaining < (lead_time * 0.5):
                risk_score = 0.85
                risk_level = "High"
                action = "Initiate expedited requisition and evaluate regional redistribution candidates."
            elif days_remaining < lead_time:
                risk_score = 0.60
                risk_level = "Medium"
                action = "Prepare regular replenishment order."
            else:
                risk_score = 0.15
                risk_level = "Low"
                action = "Stock levels adequate. Continue routine monitoring."

            est_stockout = date.today() + timedelta(days=int(days_remaining)) if days_remaining < 365 else None

            drivers = []
            if usable_stock < medicine.minimum_stock_level:
                drivers.append("Current stock below facility safety buffer threshold")
            if days_remaining < lead_time:
                drivers.append(f"Days of stock ({round(days_remaining, 1)}) is less than supplier lead time ({medicine.lead_time_days} days)")
            if inv.average_monthly_consumption > 50:
                drivers.append("High monthly consumption volume")

            results.append(
                StockoutRiskResponse(
                    facility_id=facility.id,
                    facility_name=facility.name,
                    medicine_id=medicine.id,
                    medicine_name=medicine.name,
                    current_stock=usable_stock,
                    projected_daily_consumption=round(daily_consumption, 2),
                    days_until_stockout=round(days_remaining, 1),
                    stockout_risk_score=round(risk_score, 2),
                    risk_level=risk_level,
                    estimated_stockout_date=est_stockout,
                    key_drivers=drivers or ["Stable consumption pattern"],
                    recommended_action=action,
                )
            )

        # Sort with most critical first
        results.sort(key=lambda r: r.stockout_risk_score, reverse=True)
        return results
