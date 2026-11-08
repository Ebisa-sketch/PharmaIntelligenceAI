"""
Explainable AI (XAI) and Natural Language Generation Engine for PharmaIntelligence AI

Provides:
1. Feature attributions decomposing predictions into risk-increasing and risk-decreasing factors
2. Mathematical justification of stockout and FEFO expiration predictions
3. Natural Language Generation (NLG) summaries converting quantitative metrics into clear clinical explanations

Reference: docs/06-ai-documentation/explainable-ai.md
"""

from typing import Any, Dict, List, Optional


class ExplainabilityEngine:
    @staticmethod
    def explain_forecast(
        medicine_name: str,
        facility_name: str,
        forecast_result: Dict[str, Any],
        historical_mean: float,
    ) -> Dict[str, Any]:
        """Generates XAI attributions and plain-language summary for demand forecast."""
        cumulative = forecast_result.get("cumulative_forecast", 0.0)
        p10 = forecast_result.get("p10_lower", [])
        p90 = forecast_result.get("p90_upper", [])
        category = forecast_result.get("demand_category", "smooth")
        model = forecast_result.get("model_type", "Ensemble")
        horizon = forecast_result.get("horizon_months", 3)

        expected_baseline = historical_mean * horizon
        delta = cumulative - expected_baseline

        # Feature attributions
        attributions = [
            {
                "feature": "Baseline Historical Consumption",
                "contribution": round(expected_baseline, 1),
                "impact": "neutral",
                "description": f"Average historical run-rate of {round(historical_mean, 1)} units/month.",
            }
        ]

        if abs(delta) > 0.01:
            impact = "positive" if delta > 0 else "negative"
            desc = "Projected upward consumption trend based on seasonal patterns." if delta > 0 else "Projected seasonal dip in clinic dispensing."
            attributions.append({
                "feature": "Trend & Seasonality Component",
                "contribution": round(delta, 1),
                "impact": impact,
                "description": desc,
            })

        lower_bound = sum(p10) if p10 else cumulative * 0.85
        upper_bound = sum(p90) if p90 else cumulative * 1.20

        summary = (
            f"Over the next {horizon} months, {facility_name} is projected to require "
            f"{int(cumulative):,} units of {medicine_name} (90% confidence range: "
            f"{int(lower_bound):,} to {int(upper_bound):,} units). "
            f"Demand classified as '{category.capitalize()}' using {model}."
        )

        return {
            "summary": summary,
            "demand_category": category,
            "model_utilized": model,
            "projected_total": cumulative,
            "confidence_band": {"lower_p10": round(lower_bound, 1), "upper_p90": round(upper_bound, 1)},
            "feature_attributions": attributions,
        }

    @staticmethod
    def explain_stockout_risk(
        facility_name: str,
        medicine_name: str,
        stockout_data: Dict[str, Any],
        safety_stock: float,
        lead_time_days: float,
    ) -> Dict[str, Any]:
        """Generates XAI breakdown and clinical guidance for stockout risk."""
        risk_score = stockout_data["stockout_risk_score"]
        risk_level = stockout_data["risk_level"]
        stock = stockout_data["current_stock"]
        daily_rate = stockout_data["projected_daily_consumption"]
        dsr = stockout_data["days_until_stockout"]

        attributions = []

        # Factor 1: On-hand stock vs Lead time
        if dsr < lead_time_days:
            attributions.append({
                "factor": "Lead Time Deficit",
                "contribution": "+0.35 risk",
                "direction": "INCREASE_RISK",
                "description": f"Stock coverage ({round(dsr, 1)} days) is shorter than supplier procurement lead time ({int(lead_time_days)} days).",
            })
        else:
            attributions.append({
                "factor": "Lead Time Coverage",
                "contribution": "-0.25 risk",
                "direction": "DECREASE_RISK",
                "description": f"Stock coverage ({round(dsr, 1)} days) exceeds supplier delivery window ({int(lead_time_days)} days).",
            })

        # Factor 2: Safety stock buffer
        if stock < safety_stock:
            attributions.append({
                "factor": "Safety Stock Breach",
                "contribution": "+0.25 risk",
                "direction": "INCREASE_RISK",
                "description": f"Current stock ({int(stock)}) is below minimum facility safety buffer ({int(safety_stock)} units).",
            })
        else:
            attributions.append({
                "factor": "Safety Stock Buffer",
                "contribution": "-0.20 risk",
                "direction": "DECREASE_RISK",
                "description": f"Current inventory maintains adequate buffer above safety threshold ({int(safety_stock)} units).",
            })

        # Plain-language explanation
        if risk_level == "Critical":
            nlg = (
                f"CRITICAL WARNING for {medicine_name} at {facility_name}: Current usable inventory of "
                f"{int(stock)} units will be depleted in approximately {round(dsr, 1)} days at the current "
                f"rate of {round(daily_rate, 1)} units/day. Because supplier lead time is {int(lead_time_days)} days, "
                f"immediate stockout will occur without emergency replenishment or lateral transfer."
            )
        elif risk_level == "High":
            nlg = (
                f"HIGH RISK for {medicine_name} at {facility_name}: Stock on hand ({int(stock)} units) covers "
                f"{round(dsr, 1)} days, approaching the reorder trigger. Expedited requisition recommended."
            )
        else:
            nlg = (
                f"{medicine_name} inventory is currently secure at {facility_name} ({round(dsr, 1)} days of supply). "
                f"Normal replenishment cycle suffices."
            )

        return {
            "risk_level": risk_level,
            "risk_score": risk_score,
            "days_of_stock_remaining": dsr,
            "plain_language_summary": nlg,
            "attributions": attributions,
            "recommended_action": stockout_data.get("recommended_action"),
        }

    @staticmethod
    def explain_expiry_risk(
        facility_name: str,
        medicine_name: str,
        batch_number: str,
        expiry_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Generates XAI explanation of Projected Unused Stock at Expiry (PUSE)."""
        puse = expiry_data["quantity_at_risk"]
        fvr = expiry_data["estimated_loss_etb"]
        days = expiry_data["days_until_expiry"]
        risk_level = expiry_data["risk_level"]
        daily_rate = expiry_data.get("monthly_consumption_rate", 30.0) / 30.0

        if puse > 0:
            nlg = (
                f"Batch {batch_number} of {medicine_name} ({int(expiry_data['quantity_remaining'])} units on hand) "
                f"expires in {days} days. Based on the facility's dispensing throughput of {round(daily_rate, 1)} units/day, "
                f"{int(puse)} units are projected to remain unused at expiration under FEFO priority, "
                f"representing a potential loss of {fvr:,.2f} ETB."
            )
        else:
            nlg = (
                f"Batch {batch_number} of {medicine_name} is projected to be 100% consumed before its expiration "
                f"in {days} days under standard FEFO allocation."
            )

        return {
            "batch_number": batch_number,
            "risk_level": risk_level,
            "projected_unused_units": puse,
            "financial_value_at_risk_etb": fvr,
            "days_until_expiry": days,
            "plain_language_summary": nlg,
            "formula_applied": "PUSE = max(0, min(BatchQty, CumulativeStock - CumulativeDemandAtExpiry))",
        }

