from typing import Any, Dict, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.services.experiment_service import ExperimentService

router = APIRouter()


@router.get("/", summary="List historical and active model experiments")
def list_experiments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[Dict[str, Any]]:
    """Lists completed and active AI model evaluation and benchmarking experiments."""
    service = ExperimentService(db)
    return service.list_experiments()


@router.get("/models", summary="List registered AI models and technical metadata")
def list_models(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[Dict[str, Any]]:
    """Returns the production and staging AI model registry with hyperparameters and provenance."""
    service = ExperimentService(db)
    return service.list_models()


@router.get("/benchmarks", summary="Retrieve formal baseline vs candidate model comparisons")
def get_benchmarks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Returns comparative evaluation metrics against transparent baselines
    across forecasting, stockout classification, expiry risk, and redistribution.
    """
    service = ExperimentService(db)
    return service.get_benchmarks()


@router.post("/run", summary="Trigger reproducible AI benchmark experiment")
def run_experiment(
    payload: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    """Executes a comparative evaluation between baseline and AI-driven supply decisions."""
    service = ExperimentService(db)
    return service.run_live_experiment(payload)
