"""Decision variable definitions for pharmaceutical inventory and allocation optimization models."""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Any


@dataclass
class SupplyChainVariables:
    """Encapsulates indexed decision variable mappings for optimization formulations.

    Attributes:
        order_quantities: Decision variables x[p, f, t] for quantity of product p ordered by facility f at period t.
        transfer_quantities: Decision variables y[p, f_src, f_dst, t] for transfer from f_src to f_dst.
        inventory_levels: State variables I[p, f, t] representing inventory on hand.
        shortage_quantities: Slack variables s[p, f, t] representing unmet demand.
        disposed_quantities: Variables w[p, f, t] representing expired or disposed units.
    """
    order_quantities: Dict[Tuple[str, str, int], Any] = field(default_factory=dict)
    transfer_quantities: Dict[Tuple[str, str, str, int], Any] = field(default_factory=dict)
    inventory_levels: Dict[Tuple[str, str, int], Any] = field(default_factory=dict)
    shortage_quantities: Dict[Tuple[str, str, int], Any] = field(default_factory=dict)
    disposed_quantities: Dict[Tuple[str, str, int], Any] = field(default_factory=dict)


def initialize_variable_indices(
    products: List[str],
    facilities: List[str],
    time_periods: List[int]
) -> Dict[str, List[Tuple]]:
    """Generates multi-index sets for supply chain optimization problem formulation.

    Args:
        products: List of product SKU identifiers.
        facilities: List of facility / depot identifiers.
        time_periods: List of discrete planning period indices.

    Returns:
        Dictionary mapping variable category names to their respective index tuples.
    """
    node_time_indices = [(p, f, t) for p in products for f in facilities for t in time_periods]
    arc_time_indices = [
        (p, f_src, f_dst, t)
        for p in products
        for f_src in facilities
        for f_dst in facilities
        if f_src != f_dst
        for t in time_periods
    ]

    return {
        "orders": node_time_indices,
        "transfers": arc_time_indices,
        "inventory": node_time_indices,
        "shortages": node_time_indices,
        "disposal": node_time_indices
    }
