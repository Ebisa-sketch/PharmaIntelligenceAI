"""Expiry and shelf-life stress scenarios for perishable pharmaceutical lots."""

from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass
class ExpiryScenario:
    """Encapsulates accelerated expiry or cold chain excursion scenarios."""
    scenario_id: str
    description: str
    shelf_life_reduction_pct: float
    affected_batches: List[str]


class ExpiryScenarioGenerator:
    """Generates shelf-life decay scenarios for perishable biologics and vaccines."""

    @staticmethod
    def generate_cold_chain_excursion(
        batches: List[str],
        shelf_life_loss_pct: float = 0.50
    ) -> ExpiryScenario:
        """Simulates temperature excursion degrading shelf-life of refrigerated batches by 50%."""
        return ExpiryScenario(
            scenario_id="COLD_CHAIN_EXCURSION",
            description="Temperature breach during regional transport reduces remaining shelf life.",
            shelf_life_reduction_pct=shelf_life_loss_pct,
            affected_batches=batches
        )
