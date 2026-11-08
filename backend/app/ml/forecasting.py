"""
Multi-Model Pharmaceutical Demand Forecaster for PharmaIntelligence AI

Implements:
1. Croston's Method & Syntetos-Boylan Approximation (SBA) for intermittent demand
2. Simple Moving Average & Exponential Smoothing
3. Gradient Boosted / Random Forest Time-Series Regressor with lag & seasonal features
4. Dynamic model dispatching via Syntetos-Boylan demand classification
5. Prediction intervals (P10, P50, P90)
6. Error metrics calculation: RMSE, MAE, MAPE, WAPE, MASE

Reference: docs/06-ai-documentation/forecasting-methodology.md
"""

from typing import Any, Dict, List, Optional, Tuple
import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor

from app.ml.syntetos_boylan import SyntetosBoylanClassifier


class DemandForecaster:
    def __init__(self, alpha: float = 0.2):
        self.alpha = alpha

    # ──────────────────────────────────────────────────────────
    # 1. Statistical & Intermittent Baselines
    # ──────────────────────────────────────────────────────────

    def croston_sba(
        self, series: List[float], horizon: int = 3, alpha: Optional[float] = None
    ) -> List[float]:
        """
        Croston's method with Syntetos-Boylan Approximation (SBA) correction factor:
        y_sba = (1 - alpha/2) * (z_hat / p_hat)
        """
        a = alpha or self.alpha
        arr = np.array(series, dtype=float)
        non_zero_idx = np.where(arr > 0)[0]

        if len(non_zero_idx) == 0:
            return [0.0] * horizon

        # Initialize
        z_hat = arr[non_zero_idx[0]]
        p_hat = 1.0
        last_idx = non_zero_idx[0]

        for i in non_zero_idx[1:]:
            p_val = i - last_idx
            z_val = arr[i]
            z_hat = z_hat + a * (z_val - z_hat)
            p_hat = p_hat + a * (p_val - p_hat)
            last_idx = i

        # Syntetos-Boylan Approximation correction factor
        forecast_val = (1.0 - a / 2.0) * (z_hat / max(1.0, p_hat))
        forecast_val = max(0.0, float(forecast_val))
        return [round(forecast_val, 2)] * horizon

    def moving_average(self, series: List[float], horizon: int = 3, window: int = 3) -> List[float]:
        """Simple Moving Average (SMA)."""
        if not series:
            return [0.0] * horizon
        k = min(window, len(series))
        val = float(np.mean(series[-k:]))
        val = max(0.0, val)
        return [round(val, 2)] * horizon

    def exponential_smoothing(
        self, series: List[float], horizon: int = 3, alpha: Optional[float] = None
    ) -> List[float]:
        """Single Exponential Smoothing."""
        a = alpha or self.alpha
        if not series:
            return [0.0] * horizon
        s = series[0]
        for val in series[1:]:
            s = a * val + (1 - a) * s
        s = max(0.0, float(s))
        return [round(s, 2)] * horizon

    # ──────────────────────────────────────────────────────────
    # 2. Machine Learning / Feature-Based Regressor
    # ──────────────────────────────────────────────────────────

    def _create_lag_features(
        self, series: List[float], max_lags: int = 3
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Builds lag-1, lag-2, lag-3, rolling mean, and rolling std features."""
        n = len(series)
        if n <= max_lags:
            return np.empty((0, max_lags + 2)), np.empty(0)

        X, y = [], []
        for i in range(max_lags, n):
            lags = [series[i - l] for l in range(1, max_lags + 1)]
            rolling_window = series[max(0, i - 3):i]
            roll_mean = float(np.mean(rolling_window))
            roll_std = float(np.std(rolling_window)) if len(rolling_window) > 1 else 0.0
            features = lags + [roll_mean, roll_std]
            X.append(features)
            y.append(series[i])

        return np.array(X), np.array(y)

    def ml_forecast(
        self, series: List[float], horizon: int = 3
    ) -> List[float]:
        """
        Gradient Boosted time-series autoregressive forecast with lag features.
        Falls back to Moving Average if series is too short for ML training.
        """
        if len(series) < 6:
            return self.moving_average(series, horizon=horizon, window=3)

        X, y = self._create_lag_features(series, max_lags=3)
        if len(X) < 3:
            return self.moving_average(series, horizon=horizon, window=3)

        model = HistGradientBoostingRegressor(
            max_iter=50, min_samples_leaf=2, random_state=42
        )
        model.fit(X, y)

        predictions = []
        current_series = list(series)

        for _ in range(horizon):
            lags = [current_series[-1], current_series[-2], current_series[-3]]
            rolling_window = current_series[-3:]
            features = lags + [float(np.mean(rolling_window)), float(np.std(rolling_window))]
            pred = float(model.predict([features])[0])
            pred = max(0.0, pred)
            predictions.append(round(pred, 2))
            current_series.append(pred)

        return predictions

    # ──────────────────────────────────────────────────────────
    # 3. Dynamic Dispatch & Forecast Orchestration
    # ──────────────────────────────────────────────────────────

    def forecast(
        self,
        historical_series: List[float],
        horizon: int = 3,
        model_override: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Classifies historical demand via Syntetos-Boylan, dispatches to appropriate model,
        and computes prediction intervals and uncertainty scores.
        """
        classification = SyntetosBoylanClassifier.classify(historical_series)
        category = classification["category"]
        selected_model = model_override or classification["recommended_model"]

        if selected_model == "croston_sba" or category in ["intermittent", "lumpy"]:
            point_forecasts = self.croston_sba(historical_series, horizon=horizon)
            active_model = "Croston-SBA"
        elif selected_model == "gradient_boosting" or category == "smooth":
            point_forecasts = self.ml_forecast(historical_series, horizon=horizon)
            active_model = "GradientBoostingRegressor"
        elif selected_model == "exponential_smoothing":
            point_forecasts = self.exponential_smoothing(historical_series, horizon=horizon)
            active_model = "ExponentialSmoothing"
        else:
            # Ensemble: Average ML and Moving Average
            ml_pred = self.ml_forecast(historical_series, horizon=horizon)
            sma_pred = self.moving_average(historical_series, horizon=horizon)
            point_forecasts = [round(0.6 * m + 0.4 * s, 2) for m, s in zip(ml_pred, sma_pred)]
            active_model = "Ensemble(GBM+SMA)"

        # Compute Uncertainty & Prediction Intervals (P10, P50, P90)
        hist_std = float(np.std(historical_series)) if len(historical_series) > 1 else 1.0
        hist_mean = float(np.mean(historical_series)) if historical_series else 1.0
        cv = hist_std / hist_mean if hist_mean > 0 else 0.2
        uncertainty_factor = max(0.10, min(0.60, cv))

        p50 = point_forecasts
        p10 = [round(max(0.0, p * (1.0 - 1.28 * uncertainty_factor)), 2) for p in p50]
        p90 = [round(p * (1.0 + 1.28 * uncertainty_factor), 2) for p in p50]

        # In-sample backtesting metrics on holdout
        metrics = self.evaluate_series(historical_series)

        return {
            "model_type": active_model,
            "demand_category": category,
            "adi": classification["adi"],
            "cv2": classification["cv2"],
            "horizon_months": horizon,
            "point_forecasts": point_forecasts,
            "p10_lower": p10,
            "p50_median": p50,
            "p90_upper": p90,
            "cumulative_forecast": round(float(sum(point_forecasts)), 2),
            "uncertainty_score": round(uncertainty_factor, 3),
            "metrics": metrics,
        }

    # ──────────────────────────────────────────────────────────
    # 4. Evaluation Metrics
    # ──────────────────────────────────────────────────────────

    def evaluate_series(self, series: List[float], test_size: int = 3) -> Dict[str, float]:
        """Calculates RMSE, MAE, MAPE, WAPE, and MASE on a train/test split."""
        if len(series) < test_size + 3:
            return {"rmse": 0.0, "mae": 0.0, "mape": 0.0, "wape": 0.0, "mase": 0.0}

        train = series[:-test_size]
        actual = np.array(series[-test_size:], dtype=float)

        # Baseline forecast using training set
        pred = np.array(self.moving_average(train, horizon=test_size), dtype=float)

        # Metrics
        errors = actual - pred
        abs_errors = np.abs(errors)
        mae = float(np.mean(abs_errors))
        rmse = float(np.sqrt(np.mean(errors ** 2)))

        # WAPE (Weighted Absolute Percentage Error)
        sum_actual = float(np.sum(actual))
        wape = (float(np.sum(abs_errors)) / sum_actual * 100.0) if sum_actual > 0 else 0.0

        # MAPE (Mean Absolute Percentage Error bounded)
        non_zero_mask = actual > 0
        if np.any(non_zero_mask):
            mape = float(np.mean(abs_errors[non_zero_mask] / actual[non_zero_mask]) * 100.0)
        else:
            mape = 0.0

        # MASE (Mean Absolute Scaled Error relative to naive)
        naive_diff = np.abs(np.diff(train))
        naive_mae = float(np.mean(naive_diff)) if len(naive_diff) > 0 and np.mean(naive_diff) > 0 else 1.0
        mase = mae / naive_mae

        return {
            "rmse": round(rmse, 2),
            "mae": round(mae, 2),
            "mape": round(min(100.0, mape), 2),
            "wape": round(min(100.0, wape), 2),
            "mase": round(mase, 3),
        }

