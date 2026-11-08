"""Evaluation metrics for time-series forecasting, classification, and inventory risk."""

from typing import Dict, Any, Sequence
import numpy as np


def calculate_forecast_metrics(y_true: Sequence[float], y_pred: Sequence[float]) -> Dict[str, float]:
    """Computes standard time-series forecasting metrics.

    Args:
        y_true: Ground truth observed quantities.
        y_pred: Predicted quantities.

    Returns:
        Dict containing MAE, RMSE, MAPE, and WAPE.
    """
    y_true_arr = np.asarray(y_true, dtype=float)
    y_pred_arr = np.asarray(y_pred, dtype=float)

    mae = float(np.mean(np.abs(y_true_arr - y_pred_arr)))
    rmse = float(np.sqrt(np.mean((y_true_arr - y_pred_arr) ** 2)))
    
    # Avoid zero division in MAPE
    non_zero_mask = y_true_arr != 0
    mape = float(np.mean(np.abs((y_true_arr[non_zero_mask] - y_pred_arr[non_zero_mask]) / y_true_arr[non_zero_mask])) * 100) if np.any(non_zero_mask) else 0.0

    total_actual = np.sum(np.abs(y_true_arr))
    wape = float(np.sum(np.abs(y_true_arr - y_pred_arr)) / total_actual * 100) if total_actual > 0 else 0.0

    return {
        "mae": mae,
        "rmse": rmse,
        "mape": mape,
        "wape": wape
    }


def calculate_classification_metrics(y_true: Sequence[int], y_pred: Sequence[int]) -> Dict[str, float]:
    """Computes binary classification metrics for stockout and risk prediction.

    Args:
        y_true: Ground truth binary labels.
        y_pred: Predicted binary labels.

    Returns:
        Dict containing accuracy, precision, recall, and f1_score.
    """
    y_true_arr = np.asarray(y_true, dtype=int)
    y_pred_arr = np.asarray(y_pred, dtype=int)

    tp = int(np.sum((y_true_arr == 1) & (y_pred_arr == 1)))
    fp = int(np.sum((y_true_arr == 0) & (y_pred_arr == 1)))
    fn = int(np.sum((y_true_arr == 1) & (y_pred_arr == 0)))
    tn = int(np.sum((y_true_arr == 0) & (y_pred_arr == 0)))

    accuracy = float((tp + tn) / len(y_true_arr)) if len(y_true_arr) > 0 else 0.0
    precision = float(tp / (tp + fp)) if (tp + fp) > 0 else 0.0
    recall = float(tp / (tp + fn)) if (tp + fn) > 0 else 0.0
    f1 = float(2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1
    }
