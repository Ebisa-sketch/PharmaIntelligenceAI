"""Objective function formulations for supply chain cost minimization and service level maximization."""

from dataclasses import dataclass
from typing import Dict, Any, Tuple


@dataclass
class CostCoefficients:
    """Cost parameters for multi-objective optimization.

    Attributes:
        holding_cost_per_unit: Holding cost per unit per period.
        stockout_penalty_per_unit: Penalty per unit of unmet critical medication demand.
        transport_cost_per_unit_km: Unit transportation cost per kilometer.
        disposal_cost_per_unit: Environmental and financial cost per expired unit.
        ordering_fixed_cost: Fixed setup cost per replenishment order.
    """
    holding_cost_per_unit: float = 0.50
    stockout_penalty_per_unit: float = 50.0
    transport_cost_per_unit_km: float = 0.05
    disposal_cost_per_unit: float = 5.0
    ordering_fixed_cost: float = 100.0


def build_total_cost_objective(
    costs: CostCoefficients,
    variables: Any,
    solver_interface: str = "ortools"
) -> Dict[str, Any]:
    """Constructs cost objective breakdown terms.

    Args:
        costs: Unit cost parameters.
        variables: Model decision variables object.
        solver_interface: Backend solver ('ortools' or 'pyomo').

    Returns:
        Dictionary of objective component descriptors.
    """
    return {
        "holding_cost_weight": costs.holding_cost_per_unit,
        "stockout_penalty_weight": costs.stockout_penalty_per_unit,
        "transport_cost_weight": costs.transport_cost_per_unit_km,
        "disposal_cost_weight": costs.disposal_cost_per_unit,
        "ordering_cost_weight": costs.ordering_fixed_cost,
        "solver": solver_interface
    }
