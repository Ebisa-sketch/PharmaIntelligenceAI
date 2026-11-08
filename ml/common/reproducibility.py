"""Utilities for deterministic execution and reproducibility across ML experiments."""

import os
import random
import numpy as np


def set_seed(seed: int = 42) -> None:
    """Sets random seeds across Python standard library, NumPy, and environment.

    Args:
        seed: Integer seed value.
    """
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)

    try:
        import torch  # type: ignore
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False
    except ImportError:
        pass
