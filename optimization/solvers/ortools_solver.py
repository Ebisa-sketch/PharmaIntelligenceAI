"""Google OR-Tools solver backend for Mixed-Integer Linear Programming (MILP)."""

import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class ORToolsSolver:
    """Wrapper around Google OR-Tools pywraplp for pharmaceutical supply chain optimization."""

    def __init__(self, solver_name: str = "CBC"):
        """Initializes OR-Tools linear solver.

        Args:
            solver_name: Underlying MILP solver name (e.g., 'CBC', 'SCIP', 'GLOP').
        """
        self.solver_name = solver_name
        self.solver = None

    def initialize_solver(self) -> None:
        """Instantiates solver backend if OR-Tools is installed."""
        try:
            from ortools.linear_solver import pywraplp  # type: ignore
            self.solver = pywraplp.Solver.CreateSolver(self.solver_name)
            if not self.solver:
                logger.warning("Could not create OR-Tools solver with backend %s", self.solver_name)
        except ImportError:
            logger.warning("ortools package is not installed.")

    def solve(self, timeout_seconds: int = 300) -> Dict[str, Any]:
        """Executes the MILP optimization run.

        Args:
            timeout_seconds: Solver time limit in seconds.

        Returns:
            Dictionary containing optimization status, objective value, and run metrics.
        """
        if self.solver is None:
            self.initialize_solver()

        if self.solver is None:
            return {
                "status": "UNAVAILABLE",
                "objective_value": None,
                "message": "OR-Tools solver backend could not be initialized."
            }

        self.solver.set_time_limit(timeout_seconds * 1000)
        status = self.solver.Solve()

        return {
            "status": str(status),
            "objective_value": self.solver.Objective().Value() if self.solver else None,
            "wall_time_ms": self.solver.wall_time() if self.solver else 0
        }
