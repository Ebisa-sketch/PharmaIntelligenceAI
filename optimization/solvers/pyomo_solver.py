"""Pyomo optimization environment integration for algebraic modeling and multi-solver dispatch."""

import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class PyomoSolver:
    """Wrapper around Pyomo ConcreteModel and solver factory (GLPK, Gurobi, CBC, Highs)."""

    def __init__(self, solver_name: str = "glpk"):
        """Initializes Pyomo solver wrapper.

        Args:
            solver_name: Solver executable name ('glpk', 'cbc', 'gurobi', 'highs').
        """
        self.solver_name = solver_name
        self.model = None

    def create_model(self) -> Any:
        """Constructs an empty Pyomo ConcreteModel."""
        try:
            import pyomo.environ as pyo  # type: ignore
            self.model = pyo.ConcreteModel(name="PharmaSupplyChainModel")
            return self.model
        except ImportError:
            logger.warning("pyomo package is not installed.")
            return None

    def solve(self, solver_options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Solves the instantiated Pyomo model.

        Args:
            solver_options: Key-value options passed to solver.

        Returns:
            Dictionary containing termination status and objective values.
        """
        try:
            import pyomo.environ as pyo  # type: ignore
            if self.model is None:
                self.create_model()

            opt = pyo.SolverFactory(self.solver_name)
            if solver_options:
                for k, v in solver_options.items():
                    opt.options[k] = v

            results = opt.solve(self.model, tee=False)
            return {
                "solver": self.solver_name,
                "status": str(results.solver.status),
                "termination_condition": str(results.solver.termination_condition),
            }
        except Exception as e:
            logger.error("Pyomo solve failed: %s", str(e))
            return {
                "solver": self.solver_name,
                "status": "ERROR",
                "error": str(e)
            }
