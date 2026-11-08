from typing import Any, Dict, Optional
from fastapi import HTTPException, status


class PharmaIntelligenceException(Exception):
    """Base exception for all domain exceptions in PharmaIntelligence AI."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class EntityNotFoundException(PharmaIntelligenceException):
    """Raised when a requested resource is not found."""
    pass


class DuplicateEntityException(PharmaIntelligenceException):
    """Raised when attempting to create an entity that already exists."""
    pass


class DataQualityValidationError(PharmaIntelligenceException):
    """Raised when uploaded or processed inventory data fails validation thresholds."""
    pass


class OptimizationInfeasibleException(PharmaIntelligenceException):
    """Raised when redistribution solver cannot find a feasible transfer schedule."""
    pass


class UnauthorizedActionException(PharmaIntelligenceException):
    """Raised when an operation is prohibited by business or security rules."""
    pass
