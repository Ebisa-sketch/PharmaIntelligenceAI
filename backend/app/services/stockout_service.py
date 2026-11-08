import json
from datetime import date, datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

from app.models.inventory import Inventory
from app.models.medicine import Medicine
from app.models.facility import Facility
from app.models.prediction import Prediction
from app.schemas.forecasting import StockoutRiskResponse
from app.ml.stockout_classifier import StockoutRiskClassifier
from app.ml.explainability import ExplainabilityEngine
from app.core.exceptions import EntityNotFoundException


class StockoutService:
    def __init__(self, db: Session):
        self.db = db
        self.classifier = StockoutRiskClassifier()

    def evaluate_facility_stockouts(
        self, facility_id: int, persist: bool = True
    ) -> List[StockoutRiskResponse]:
        """
        Evaluates stockout risks across all medicines at a facility using the ML classifier:
        - Incorporates Days of Stock Remaining (DSR)
        - Computes calibrated probability of stockout within procurement lead time
        - Generates Explainable AI (XAI) feature attributions and clinical guidance
        - Optionally persists predictions into the `predictions` table
        """
        facility = self.db.get(Facility, facility_id)
        if not facility:
            raise EntityNotFoundException(f"Facility ID {facility_id} not found.")

        inventories = self.db.query(Inventory).filter(Inventory.facility_id == facility_id).all()
        results: List[StockoutRiskResponse] = []
        predictions_to_persist = []

        for inv in inventories:
            medicine = self.db.get(Medicine, inv.medicine_id)
            if not medicine:
                continue

            daily_consumption = (inv.average_monthly_consumption / 30.0) if inv.average_monthly_consumption > 0 else 2.0
            usable_stock = max(0.0, inv.usable_stock)
            lead_time = float(medicine.lead_time_days)
            safety_stock = float(medicine.minimum_stock_level)

            # Predict risk using ML classifier
            risk_data = self.classifier.predict_risk(
                facility_id=facility.id,
                facility_name=facility.name,
                medicine_id=medicine.id,
                medicine_name=medicine.name,
                usable_stock=usable_stock,
                daily_consumption=daily_consumption,
                lead_time_days=lead_time,
                safety_stock=safety_stock,
            )

            # Explainability
            xai = ExplainabilityEngine.explain_stockout_risk(
                facility_name=facility.name,
                medicine_name=medicine.name,
                stockout_data=risk_data,
                safety_stock=safety_stock,
                lead_time_days=lead_time,
            )

            response_item = StockoutRiskResponse(
                facility_id=facility.id,
                facility_name=facility.name,
                medicine_id=medicine.id,
                medicine_name=medicine.name,
                current_stock=risk_data["current_stock"],
                projected_daily_consumption=risk_data["projected_daily_consumption"],
                days_until_stockout=risk_data["days_until_stockout"],
                stockout_risk_score=risk_data["stockout_risk_score"],
                risk_level=risk_data["risk_level"],
                estimated_stockout_date=risk_data["estimated_stockout_date"],
                key_drivers=risk_data["key_drivers"],
                recommended_action=risk_data["recommended_action"],
                explanation=xai["plain_language_summary"],
                attributions=xai["attributions"],
            )
            results.append(response_item)

            if persist:
                pred = Prediction(
                    facility_id=facility.id,
                    medicine_id=medicine.id,
                    risk_type="Stockout",
                    risk_score=risk_data["stockout_risk_score"],
                    risk_level=risk_data["risk_level"],
                    estimated_stockout_date=risk_data["estimated_stockout_date"],
                    explanation=json.dumps({
                        "summary": xai["plain_language_summary"],
                        "attributions": xai["attributions"],
                        "days_remaining": risk_data["days_until_stockout"],
                    }),
                    prediction_date=datetime.now(timezone.utc),
                )
                predictions_to_persist.append(pred)

        if persist and predictions_to_persist:
            self.db.add_all(predictions_to_persist)
            self.db.commit()

        # Sort: Critical first, then by highest risk score
        results.sort(key=lambda r: r.stockout_risk_score, reverse=True)
        return results
