"""Machine Learning configuration management module."""

import os
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from pathlib import Path


@dataclass
class MLConfig:
    """Master configuration for ML training and inference pipelines."""
    data_dir: Path = Path("data")
    artifacts_dir: Path = Path("artifacts")
    models_dir: Path = Path("models")
    random_seed: int = 42
    test_size: float = 0.2
    validation_size: float = 0.1
    forecast_horizon_days: int = 30
    stockout_threshold_days: int = 7
    expiry_risk_threshold_days: int = 90
    model_params: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_env(cls) -> "MLConfig":
        """Instantiate configuration from environment variables."""
        return cls(
            data_dir=Path(os.getenv("DATA_DIR", "data")),
            artifacts_dir=Path(os.getenv("ARTIFACTS_DIR", "artifacts")),
            models_dir=Path(os.getenv("MODELS_DIR", "models")),
            random_seed=int(os.getenv("RANDOM_SEED", "42")),
            test_size=float(os.getenv("TEST_SIZE", "0.2")),
            forecast_horizon_days=int(os.getenv("FORECAST_HORIZON_DAYS", "30")),
        )
