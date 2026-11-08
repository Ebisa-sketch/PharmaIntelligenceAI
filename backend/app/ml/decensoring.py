"""
Stockout De-censoring Transformer for PharmaIntelligence AI

Implements RULE-C01 & RULE-C02 from the Data Cleaning Protocol:
- In-stock ratio calculation: R = (T - S) / T
- Minor stockout (R >= 0.90): No adjustment (y_adj = y_obs)
- Moderate stockout (0.10 <= R < 0.90): Proportional adjustment (y_adj = y_obs / R)
- Severe stockout (R < 0.10): Censored observation; impute using rolling median of in-stock periods
- Distinguishes True Zero (in-stock > 0, consumption = 0) from Censored Zero (stockout = 0)

Reference: docs/05-data-documentation/data-cleaning-rules.md §Rule Set C
           docs/06-ai-documentation/forecasting-methodology.md §3
"""

from typing import Any, Dict, List, Optional
import numpy as np
import pandas as pd


class StockoutDecensoringTransformer:
    def __init__(self, default_operational_days: int = 30):
        self.default_operational_days = default_operational_days

    def decensor_point(
        self,
        observed_consumption: float,
        stockout_days: int,
        operational_days: Optional[int] = None,
        closing_stock: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        De-censors a single observation period.
        """
        T = operational_days or self.default_operational_days
        S = max(0, min(T, stockout_days))
        R = (T - S) / T if T > 0 else 1.0

        is_true_zero = False
        is_censored_zero = False
        classification = "UNCENSORED"
        adjusted_consumption = observed_consumption

        if observed_consumption == 0:
            if closing_stock is not None and closing_stock > 0:
                is_true_zero = True
                classification = "TRUE_ZERO"
                adjusted_consumption = 0.0
            elif S >= T or (closing_stock is not None and closing_stock <= 0):
                is_censored_zero = True
                classification = "CENSORED_ZERO"
                # Will be imputed in series context
                adjusted_consumption = np.nan

        if not is_true_zero and not is_censored_zero:
            if R >= 0.90:
                # Minor stockout (<3 days)
                classification = "UNCENSORED"
                adjusted_consumption = observed_consumption
            elif 0.10 <= R < 0.90:
                # Moderate stockout: Scale up to estimated full-month potential
                classification = "ADJUSTED"
                adjusted_consumption = observed_consumption / R
            else:
                # Severe stockout (out of stock >90% of month): Flag for imputation
                classification = "SEVERELY_CENSORED"
                adjusted_consumption = np.nan

        return {
            "observed_consumption": observed_consumption,
            "stockout_days": S,
            "operational_days": T,
            "in_stock_ratio": round(R, 3),
            "adjusted_consumption": round(adjusted_consumption, 2) if not np.isnan(adjusted_consumption) else np.nan,
            "classification": classification,
        }

    def transform_series(
        self,
        series: List[Dict[str, Any]],
        rolling_window: int = 6,
    ) -> List[Dict[str, Any]]:
        """
        De-censors an entire chronological time-series of monthly records.
        Each record should contain 'observed_consumption' and 'stockout_days'.
        Optionally contains 'operational_days' and 'closing_stock'.
        Imputes severely censored periods using rolling median of in-stock periods.
        """
        results = []
        for record in series:
            obs = float(record.get("observed_consumption", 0.0))
            stk_days = int(record.get("stockout_days", 0))
            op_days = record.get("operational_days")
            closing = record.get("closing_stock")
            point_res = self.decensor_point(obs, stk_days, op_days, closing)
            results.append(point_res)

        # Impute NaNs using rolling median of valid in-stock observations
        values = [r["adjusted_consumption"] for r in results]
        valid_values = [v for v in values if not np.isnan(v)]
        fallback_median = float(np.median(valid_values)) if valid_values else 10.0

        for i, r in enumerate(results):
            if np.isnan(r["adjusted_consumption"]):
                # Look back in window
                start_idx = max(0, i - rolling_window)
                local_window = [
                    results[k]["adjusted_consumption"]
                    for k in range(start_idx, i)
                    if not np.isnan(results[k]["adjusted_consumption"])
                ]
                if not local_window:
                    # Look forward if early in series
                    local_window = [
                        results[k]["adjusted_consumption"]
                        for k in range(i + 1, min(len(results), i + rolling_window + 1))
                        if not np.isnan(results[k]["adjusted_consumption"])
                    ]

                imputed_val = float(np.median(local_window)) if local_window else fallback_median
                r["adjusted_consumption"] = round(max(0.0, imputed_val), 2)
                r["classification"] = "IMPUTED"

        return results

