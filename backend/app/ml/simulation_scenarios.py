"""
Redistribution Simulation Scenarios for PharmaIntelligence AI

Compares operational policies and disaster/epidemic scenarios:
1. Baseline (Isolated Operation): Clinics do not share inventory.
2. Full Collaborative Network: Open regional lateral transfers (D_max = 150 km).
3. Local Primary Clusters: Transfers limited to immediate health post catchment (D_max = 40 km).
4. Epidemic Demand Spike: 2.5x demand surge in high-risk zones (e.g., malaria / cholera outbreak).

Evaluates key performance indicators (KPIs):
- Unmet Shortages
- Expired Medicine Wastage (Units & ETB)
- Lateral Transfers Executed & Transport Costs
- Net Economic Benefit
- Service Level / Fill Rate (%)
"""

from typing import Any, Dict, List, Optional
import copy

from app.ml.redistribution_optimizer import MILPRedistributionOptimizer


class RedistributionSimulator:
    def __init__(self, optimizer: Optional[MILPRedistributionOptimizer] = None):
        self.optimizer = optimizer or MILPRedistributionOptimizer()

    def run_scenario(
        self,
        scenario_type: str,
        facilities: List[Dict[str, Any]],
        medicines: List[Dict[str, Any]],
        inventories: List[Dict[str, Any]],
        batches: List[Dict[str, Any]],
        horizon_months: int = 6,
    ) -> Dict[str, Any]:
        """Runs the selected simulation scenario and returns comparative KPIs."""
        scenario_type = scenario_type.lower()

        # Deep copy to keep base inputs pristine
        sim_facilities = copy.deepcopy(facilities)
        sim_medicines = copy.deepcopy(medicines)
        sim_inventories = copy.deepcopy(inventories)
        sim_batches = copy.deepcopy(batches)

        # Baseline: Isolated operation (no transfers)
        baseline_kpis = self._evaluate_isolated_baseline(
            sim_inventories, sim_batches, sim_medicines
        )

        # Configure scenario-specific parameters
        if scenario_type == "baseline_isolated":
            desc = "Independent facility operation with zero lateral stock transfers."
            scenario_kpis = baseline_kpis
            opt_result = {"allocations": []}

        elif scenario_type == "collaborative_network":
            desc = "Full regional collaborative network with dynamic multi-facility lateral redistribution (max 150 km)."
            opt_result = self.optimizer.solve(
                sim_facilities, sim_medicines, sim_inventories, sim_batches
            )
            scenario_kpis = self._evaluate_with_transfers(
                baseline_kpis, opt_result["allocations"], sim_medicines
            )

        elif scenario_type == "local_cluster":
            desc = "Localized primary cluster redistribution constrained to immediate neighboring clinics (max 40 km)."
            local_opt = MILPRedistributionOptimizer(max_distance_km=40.0)
            opt_result = local_opt.solve(
                sim_facilities, sim_medicines, sim_inventories, sim_batches
            )
            scenario_kpis = self._evaluate_with_transfers(
                baseline_kpis, opt_result["allocations"], sim_medicines
            )

        elif scenario_type == "epidemic_spike":
            desc = "Severe epidemic morbidity surge (2.5x demand spike on antibiotics and antimalarials in target facilities)."
            # Double deficits on target anti-infectives
            for inv in sim_inventories:
                m_id = inv["medicine_id"]
                med = next((m for m in sim_medicines if m["id"] == m_id), None)
                if med and med.get("category") in ["Antibiotics", "Antimalarials"]:
                    inv["usable_stock"] = max(0.0, inv.get("usable_stock", 0.0) * 0.3)

            opt_result = self.optimizer.solve(
                sim_facilities, sim_medicines, sim_inventories, sim_batches
            )
            # Recompute baseline under epidemic
            epidemic_baseline = self._evaluate_isolated_baseline(
                sim_inventories, sim_batches, sim_medicines
            )
            scenario_kpis = self._evaluate_with_transfers(
                epidemic_baseline, opt_result["allocations"], sim_medicines
            )
            baseline_kpis = epidemic_baseline
        else:
            desc = "Standard regional collaborative network."
            opt_result = self.optimizer.solve(
                sim_facilities, sim_medicines, sim_inventories, sim_batches
            )
            scenario_kpis = self._evaluate_with_transfers(
                baseline_kpis, opt_result["allocations"], sim_medicines
            )

        # Compute improvements
        shortage_diff = baseline_kpis["total_shortages_unmet"] - scenario_kpis["total_shortages_unmet"]
        shortage_reduc_pct = (
            (shortage_diff / baseline_kpis["total_shortages_unmet"] * 100.0)
            if baseline_kpis["total_shortages_unmet"] > 0 else 0.0
        )
        waste_diff = baseline_kpis["total_expired_loss_etb"] - scenario_kpis["total_expired_loss_etb"]
        waste_reduc_pct = (
            (waste_diff / baseline_kpis["total_expired_loss_etb"] * 100.0)
            if baseline_kpis["total_expired_loss_etb"] > 0 else 0.0
        )

        return {
            "scenario_type": scenario_type,
            "scenario_name": scenario_type.replace("_", " ").title(),
            "description": desc,
            "facilities_evaluated": len(facilities),
            "medicines_evaluated": len(medicines),
            "baseline_kpis": baseline_kpis,
            "scenario_kpis": scenario_kpis,
            "improvement_summary": {
                "shortage_reduction_units": round(shortage_diff, 1),
                "shortage_reduction_percent": round(max(0.0, shortage_reduc_pct), 1),
                "wastage_savings_etb": round(waste_diff, 2),
                "wastage_reduction_percent": round(max(0.0, waste_reduc_pct), 1),
                "net_economic_benefit_etb": round(scenario_kpis["net_economic_benefit_etb"], 2),
                "service_level_gain_percent": round(
                    scenario_kpis["service_level_percent"] - baseline_kpis["service_level_percent"], 1
                ),
                "transfers_recommended_count": len(opt_result.get("allocations", [])),
            },
        }

    def _evaluate_isolated_baseline(
        self,
        inventories: List[Dict[str, Any]],
        batches: List[Dict[str, Any]],
        medicines: List[Dict[str, Any]],
    ) -> Dict[str, float]:
        """Calculates isolated operational metrics without lateral transfers."""
        med_map = {m["id"]: m for m in medicines}
        total_shortage = 0.0
        total_demand = 0.0

        for inv in inventories:
            med = med_map.get(inv["medicine_id"])
            if not med:
                continue
            ss = float(med.get("minimum_stock_level", 0.0))
            usable = max(0.0, float(inv.get("usable_stock", 0.0)))
            total_demand += ss * 2.0
            if usable < ss:
                total_shortage += (ss - usable)

        total_expired_units = 0.0
        total_expired_loss = 0.0
        for b in batches:
            if b.get("status") == "Expired":
                qty = float(b.get("quantity_remaining", 0.0))
                cost = float(b.get("unit_cost_etb", 0.0))
                total_expired_units += qty
                total_expired_loss += qty * cost

        fill_rate = ((total_demand - total_shortage) / total_demand * 100.0) if total_demand > 0 else 100.0
        return {
            "total_shortages_unmet": round(total_shortage, 1),
            "total_expired_units": round(total_expired_units, 1),
            "total_expired_loss_etb": round(total_expired_loss, 2),
            "total_transferred_units": 0.0,
            "total_transport_cost_etb": 0.0,
            "net_economic_benefit_etb": 0.0,
            "service_level_percent": round(max(0.0, min(100.0, fill_rate)), 1),
        }

    def _evaluate_with_transfers(
        self,
        baseline: Dict[str, float],
        allocations: List[Dict[str, Any]],
        medicines: List[Dict[str, Any]],
    ) -> Dict[str, float]:
        """Updates baseline KPIs after accounting for lateral redistribution transfers."""
        transferred_units = sum(a["quantity_recommended"] for a in allocations)
        transport_cost = sum(a["estimated_transfer_cost_etb"] for a in allocations)
        prevented_loss = sum(a["prevented_wastage_cost_etb"] for a in allocations)

        remaining_shortage = max(0.0, baseline["total_shortages_unmet"] - transferred_units)
        remaining_loss = max(0.0, baseline["total_expired_loss_etb"] - prevented_loss)
        net_benefit = round(prevented_loss - transport_cost, 2)

        # Improved service level
        base_service = baseline["service_level_percent"]
        service_improvement = (transferred_units / max(1.0, baseline["total_shortages_unmet"])) * (100.0 - base_service)
        new_service_level = min(99.5, base_service + service_improvement)

        return {
            "total_shortages_unmet": round(remaining_shortage, 1),
            "total_expired_units": round(max(0.0, baseline["total_expired_units"] - transferred_units * 0.5), 1),
            "total_expired_loss_etb": round(remaining_loss, 2),
            "total_transferred_units": round(transferred_units, 1),
            "total_transport_cost_etb": round(transport_cost, 2),
            "net_economic_benefit_etb": net_benefit,
            "service_level_percent": round(new_service_level, 1),
        }
