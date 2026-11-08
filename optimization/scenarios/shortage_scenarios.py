"""Shortage and surge scenario generation for stress-testing pharmaceutical supply networks."""

from dataclasses import dataclass
from typing import Dict, List, Any
import numpy as np


@dataclass
class ShortageScenario:
    """Defines shock parameters for epidemic surge or critical supplier stockout."""
    scenario_id: str
    description: str
    affected_products: List[str]
    demand_multiplier: float = 1.0
    supply_reduction_factor: float = 0.0


class ShortageScenarioGenerator:
    """Generates stressed supply/demand conditions across clinical product categories."""

    @staticmethod
    def generate_epidemic_surge(
        products: List[str],
        surge_multiplier: float = 2.5
    ) -> ShortageScenario:
        """Generates demand spike scenario across respiratory/antiviral medications."""
        return ShortageScenario(
            scenario_id="EPIDEMIC_SURGE",
            description="Sudden 2.5x demand spike across designated therapeutic classes.",
            affected_products=products,
            demand_multiplier=surge_multiplier,
            supply_reduction_factor=0.0
        )

    @staticmethod
    def generate_supplier_disruption(
        products: List[str],
        disruption_factor: float = 0.8
    ) -> ShortageScenario:
        """Generates upstream active pharmaceutical ingredient (API) disruption scenario."""
        return ShortageScenario(
            scenario_id="SUPPLIER_DISRUPTION",
            description="80% reduction in inbound replenishment deliveries due to port/API outage.",
            affected_products=products,
            demand_multiplier=1.0,
            supply_reduction_factor=disruption_factor
        )
