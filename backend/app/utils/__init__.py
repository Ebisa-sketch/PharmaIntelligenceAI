"""Utility functions and common helpers for PharmaIntelligence AI."""
import math
from datetime import datetime, timezone
from typing import Any, Dict


def utc_now() -> datetime:
    """Return timezone-aware current UTC datetime."""
    return datetime.now(timezone.utc)


def sanitize_nan(val: Any) -> Any:
    """Replace NaN / Inf values with None or safe serializable values."""
    if isinstance(val, float) and (math.isnan(val) or math.isinf(val)):
        return None
    return val
