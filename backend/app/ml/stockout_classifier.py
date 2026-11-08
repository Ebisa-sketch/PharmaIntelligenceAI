"""
Stockout Risk Intelligence Classifier for PharmaIntelligence AI

Implements probabilistic classification of medicine stockouts over 30/60-day horizons.
Features:
- DSR / Lead Time coverage ratio
- Safety Stock buffer ratio: (Usable Stock - SS) / SS
- Demand volatility ratio: P90 / Mean
- Historical demand CV
- Historical stockout frequency

Reference: docs/06-ai-documentation/stockout-risk-methodology.md
"""

from datetime import date, timedelta
from typing import Any, Dict, List, Optional
import numpy as np
from sklearn.ensemble import RandomForestClassifier


class StockoutRiskClassifier:
    def __init__(self):
        # Initialize internal calibrated classifier
        self.model = RandomForestClassifier(
            n_estimators=50, max_depth=5, random_state=42
        )
        self._is_trained = False
        self._bootstrap_model()

    def _bootstrap_model(self):
        """Pre-fits model on synthetic operational scenarios so it can predict immediately."""
        # Feature columns: [dsr_lead_ratio, safety_buffer_ratio, dsr_days, p90_mean_ratio, demand_cv, hist_stockout_rate]
        # Synthetic domain boundary patterns:
        X_train = np.array([
            [0.2, -0.8, 5.0, 1.8, 0.6, 0.4],   # Immediate stockout danger
            [0.4, -0.5, 10.0, 1.5, 0.4, 0.3],  # High danger
            [0.7, -0.1, 18.0, 1.3, 0.3, 0.2],  # Moderate danger
            [1.0, 0.2, 28.0, 1.2, 0.2, 0.1],   # Low-medium risk
            [1.5, 0.8, 45.0, 1.1, 0.15, 0.0],  # Safe
            [2.5, 1.5, 75.0, 1.05, 0.10, 0.0], # Very safe
            [0.1, -1.0, 2.0, 2.0, 0.7, 0.5],   # Critical
            [0.9, 0.0, 25.0, 1.4, 0.35, 0.1],  # Warning
            [1.8, 1.0, 50.0, 1.1, 0.12, 0.0],  # Safe
            [0.3, -0.6, 8.0, 1.6, 0.5, 0.35],  # High
        ])
        y_train = np.array([1, 1, 1, 0, 0, 0, 1, 0, 0, 1])
        self.model.fit(X_train, y_train)
        self._is_trained = True

    def extract_features(
        self,
        usable_stock: float,
        daily_consumption: float,
        lead_time_days: float,
        safety_stock: float,
        p90_demand: Optional[float] = None,
        demand_cv: Optional[float] = None,
        historical_stockouts: int = 0,
    ) -> np.ndarray:
        """Extracts normalized feature vector for classification."""
        daily_rate = max(0.01, daily_consumption)
        lead_time = max(1.0, lead_time_days)
        ss = max(1.0, safety_stock)

        # Days of Stock Remaining (DSR)
        dsr = usable_stock / daily_rate
        dsr_lead_ratio = dsr / lead_time
        safety_buffer_ratio = (usable_stock - ss) / ss

        mean_monthly = daily_rate * 30.0
        p90 = p90_demand if p90_demand is not None else (mean_monthly * 1.3)
        p90_mean_ratio = p90 / max(1.0, mean_monthly)

        cv = demand_cv if demand_cv is not None else 0.25
        hist_stockout_rate = min(1.0, historical_stockouts / 12.0)

        return np.array([
            dsr_lead_ratio,
            safety_buffer_ratio,
            dsr,
            p90_mean_ratio,
            cv,
            hist_stockout_rate,
        ])

    def predict_risk(
        self,
        facility_id: int,
        facility_name: str,
        medicine_id: int,
        medicine_name: str,
        usable_stock: float,
        daily_consumption: float,
        lead_time_days: float,
        safety_stock: float,
        p90_demand: Optional[float] = None,
        demand_cv: Optional[float] = None,
        historical_stockouts: int = 0,
    ) -> Dict[str, Any]:
        """
        Predicts stockout probability and operational risk level.
        """
        features = self.extract_features(
            usable_stock=usable_stock,
            daily_consumption=daily_consumption,
            lead_time_days=lead_time_days,
            safety_stock=safety_stock,
            p90_demand=p90_demand,
            demand_cv=demand_cv,
            historical_stockouts=historical_stockouts,
        )

        daily_rate = max(0.01, daily_consumption)
        days_remaining = max(0.0, usable_stock / daily_rate)

        # Predict ML probability
        probs = self.model.predict_proba([features])[0]
        ml_prob = float(probs[1]) if len(probs) > 1 else 0.0

        # Heuristic calibration based on deterministic DSR
        if usable_stock <= 0:
            calibrated_prob = 1.0
            risk_level = "Critical"
            action = "Stockout active. Issue immediate emergency order or inter-facility transfer."
        elif days_remaining < (lead_time_days * 0.5) or ml_prob >= 0.70:
            calibrated_prob = max(0.75, ml_prob)
            risk_level = "Critical"
            action = "High stockout danger. Expedite procurement and prepare lateral transfer requisition."
        elif days_remaining < lead_time_days or ml_prob >= 0.40:
            calibrated_prob = max(0.45, ml_prob)
            risk_level = "High"
            action = "Reorder point reached. Initiate standard replenishment requisition."
        elif days_remaining < (lead_time_days * 1.5):
            calibrated_prob = max(0.20, ml_prob)
            risk_level = "Medium"
            action = "Inventory adequate but within safety buffer. Monitor weekly consumption."
        else:
            calibrated_prob = min(0.15, ml_prob)
            risk_level = "Low"
            action = "Stock levels secure. Continue routine distribution schedule."

        # Compute estimated stockout date
        stockout_date = None
        if days_remaining < 365:
            stockout_date = date.today() + timedelta(days=int(days_remaining))

        # Identify key drivers
        key_drivers = []
        if usable_stock <= 0:
            key_drivers.append("Physical stock exhausted (0 units on hand)")
        if days_remaining < lead_time_days:
            key_drivers.append(f"Stock coverage ({round(days_remaining, 1)}d) is below supplier lead time ({int(lead_time_days)}d)")
        if usable_stock < safety_stock:
            key_drivers.append("Usable inventory has breached the minimum safety stock threshold")
        if (p90_demand or 0) > (daily_consumption * 35):
            key_drivers.append("Elevated demand volatility (P90 spike risk)")
        if not key_drivers:
            key_drivers.append("Stable consumption within acceptable safety stock margins")

        return {
            "facility_id": facility_id,
            "facility_name": facility_name,
            "medicine_id": medicine_id,
            "medicine_name": medicine_name,
            "current_stock": round(usable_stock, 2),
            "projected_daily_consumption": round(daily_consumption, 2),
            "days_until_stockout": round(days_remaining, 1),
            "stockout_risk_score": round(calibrated_prob, 2),
            "risk_level": risk_level,
            "estimated_stockout_date": stockout_date,
            "key_drivers": key_drivers,
            "recommended_action": action,
        }

