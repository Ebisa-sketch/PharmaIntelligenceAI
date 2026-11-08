"""Logistics and transport disruption scenario definitions."""

from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class TransportDisruptionScenario:
    """Models transit corridor closures, severe weather, or freight rate spikes."""
    scenario_id: str
    description: str
    blocked_corridors: List[Tuple[str, str]]
    lead_time_delay_days: int
    freight_cost_multiplier: float = 1.0


class TransportScenarioGenerator:
    """Generates logistics network stress test scenarios."""

    @staticmethod
    def generate_corridor_closure(
        corridors: List[Tuple[str, str]],
        delay_days: int = 5
    ) -> TransportDisruptionScenario:
        """Simulates lane shutdown forcing re-routing and adding transit delay."""
        return TransportDisruptionScenario(
            scenario_id="CORRIDOR_SHUTDOWN",
            description="Major highway/port transit interruption on key distribution arcs.",
            blocked_corridors=corridors,
            lead_time_delay_days=delay_days,
            freight_cost_multiplier=1.75
        )
