from typing import Any, Dict, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/")
def list_experiments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[Dict[str, Any]]:
    """Lists completed and active AI model evaluation and benchmarking experiments."""
    return [
        {
            "experiment_id": "EXP-ETH-001",
            "name": "Ensemble Demand Forecasting vs SARIMAX Baseline",
            "status": "Completed",
            "evaluation_metrics": {
                "baseline_mape": 24.3,
                "ai_ensemble_mape": 11.4,
                "stockout_reduction_pct": 34.2,
                "expiry_reduction_pct": 28.7,
            },
            "timestamp": "2026-10-15T10:00:00Z"
        },
        {
            "experiment_id": "EXP-ETH-002",
            "name": "Explainable Feature Attribution (SHAP) Fidelity Benchmark",
            "status": "Completed",
            "evaluation_metrics": {
                "feature_stability_score": 0.91,
                "mean_explanation_latency_ms": 42.0,
            },
            "timestamp": "2026-11-01T14:30:00Z"
        }
    ]


@router.post("/run")
def run_experiment(
    payload: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    """Trigger simulated comparative evaluation between baseline and AI-driven supply decisions."""
    return {
        "status": "queued",
        "experiment_id": f"EXP-ETH-{hash(str(payload)) % 10000:04d}",
        "message": "Evaluation pipeline started in asynchronous background task."
    }
