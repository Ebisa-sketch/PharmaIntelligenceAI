"""
Syntetos-Boylan Demand Categorization Framework

Classifies time-series demand patterns into four categories:
1. Smooth (ADI < 1.32, CV^2 < 0.49) -> High-volume, predictable
2. Intermittent (ADI >= 1.32, CV^2 < 0.49) -> Infrequent regular demand
3. Erratic (ADI < 1.32, CV^2 >= 0.49) -> Frequent highly variable sizes
4. Lumpy (ADI >= 1.32, CV^2 >= 0.49) -> Infrequent highly variable sizes

Reference: docs/06-ai-documentation/forecasting-methodology.md §2
"""

from typing import Any, Dict, List
import numpy as np


class SyntetosBoylanClassifier:
    ADI_CUTOFF: float = 1.32
    CV2_CUTOFF: float = 0.49

    @classmethod
    def classify(cls, series: List[float]) -> Dict[str, Any]:
        """
        Classifies a demand time series.
        Returns ADI, CV^2, demand_category, and recommended_model.
        """
        if not series or len(series) == 0:
            return {
                "adi": 1.0,
                "cv2": 0.0,
                "category": "smooth",
                "recommended_model": "ensemble",
            }

        arr = np.array(series, dtype=float)
        non_zero = arr[arr > 0]
        n_total = len(arr)
        n_non_zero = len(non_zero)

        if n_non_zero == 0:
            return {
                "adi": float(n_total),
                "cv2": 0.0,
                "category": "intermittent",
                "recommended_model": "croston",
            }

        # Average Inter-Demand Interval
        adi = n_total / n_non_zero

        # Squared Coefficient of Variation of non-zero demands
        mean_non_zero = float(np.mean(non_zero))
        std_non_zero = float(np.std(non_zero, ddof=1)) if n_non_zero > 1 else 0.0
        cv2 = (std_non_zero / mean_non_zero) ** 2 if mean_non_zero > 0 else 0.0

        adi = round(float(adi), 3)
        cv2 = round(float(cv2), 3)

        # Categorize
        if adi < cls.ADI_CUTOFF and cv2 < cls.CV2_CUTOFF:
            category = "smooth"
            recommended_model = "gradient_boosting"
        elif adi >= cls.ADI_CUTOFF and cv2 < cls.CV2_CUTOFF:
            category = "intermittent"
            recommended_model = "croston_sba"
        elif adi < cls.ADI_CUTOFF and cv2 >= cls.CV2_CUTOFF:
            category = "erratic"
            recommended_model = "quantile_regression"
        else:
            category = "lumpy"
            recommended_model = "tsb"

        return {
            "adi": adi,
            "cv2": cv2,
            "category": category,
            "recommended_model": recommended_model,
        }

