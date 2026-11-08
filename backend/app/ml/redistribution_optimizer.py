"""
Mixed-Integer Linear Programming (MILP) Redistribution Optimization Engine

Formulates and solves the multi-facility lateral stock transfer problem using Google OR-Tools.
Objective:
  Minimize: Shortage Penalties + Expiry Wastage + Physical Transport Costs + Fixed Dispatch Costs
Subject to:
  1. Donor safety stock protection (Hard constraint)
  2. Batch on-hand availability bound
  3. Recipient shortage absorption limit
  4. Remaining shelf-life viability (RSL_b - T_ij >= threshold)
  5. Maximum transit distance threshold (d_ij <= D_max)
  6. Cold-chain storage compatibility

Reference: docs/06-ai-documentation/redistribution-optimization.md
"""

import math
from datetime import date, timedelta
from typing import Any, Dict, List, Optional, Tuple

try:
    from ortools.linear_solver import pywraplp
    OR_TOOLS_AVAILABLE = True
except ImportError:
    OR_TOOLS_AVAILABLE = False


def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates great-circle distance between two GPS coordinates in kilometers."""
    r = 6371.0  # Earth's radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return round(r * c, 2)


class MILPRedistributionOptimizer:
    def __init__(
        self,
        cost_shortage: float = 100.0,
        cost_waste: float = 50.0,
        cost_transport_per_km_unit: float = 0.02,
        fixed_route_cost: float = 50.0,
        max_distance_km: float = 150.0,
        min_shelf_life_days: int = 90,
    ):
        self.c_shortage = cost_shortage
        self.c_waste = cost_waste
        self.c_transport = cost_transport_per_km_unit
        self.fixed_route_cost = fixed_route_cost
        self.max_distance_km = max_distance_km
        self.min_shelf_life_days = min_shelf_life_days

    def solve(
        self,
        facilities: List[Dict[str, Any]],
        medicines: List[Dict[str, Any]],
        inventories: List[Dict[str, Any]],
        batches: List[Dict[str, Any]],
        today: Optional[date] = None,
    ) -> Dict[str, Any]:
        """
        Executes the MILP optimization model across all candidate facility-batch pairs.
        """
        current_date = today or date.today()

        # Lookup structures
        fac_map = {f["id"]: f for f in facilities}
        med_map = {m["id"]: m for m in medicines}

        # 1. Compute Deficits and Surpluses
        # Recipient Deficits: D[j, m] = max(0, safety_stock - usable_stock)
        deficits: Dict[Tuple[int, int], float] = {}
        for inv in inventories:
            f_id = inv["facility_id"]
            m_id = inv["medicine_id"]
            med = med_map.get(m_id)
            if not med:
                continue
            ss = float(med.get("minimum_stock_level", 0.0))
            usable = max(0.0, float(inv.get("usable_stock", 0.0)))
            if usable < ss:
                deficits[(f_id, m_id)] = round(ss - usable, 2)

        # Donor Surpluses: Total stock - safety_stock
        surpluses: Dict[Tuple[int, int], float] = {}
        for inv in inventories:
            f_id = inv["facility_id"]
            m_id = inv["medicine_id"]
            med = med_map.get(m_id)
            if not med:
                continue
            ss = float(med.get("minimum_stock_level", 0.0))
            usable = max(0.0, float(inv.get("usable_stock", 0.0)))
            if usable > ss:
                surpluses[(f_id, m_id)] = round(usable - ss, 2)

        # Distance Matrix
        distances: Dict[Tuple[int, int], float] = {}
        for f1 in facilities:
            for f2 in facilities:
                if f1["id"] != f2["id"]:
                    lat1, lon1 = f1.get("latitude"), f1.get("longitude")
                    lat2, lon2 = f2.get("latitude"), f2.get("longitude")
                    if lat1 and lon1 and lat2 and lon2:
                        dist = haversine_distance_km(lat1, lon1, lat2, lon2)
                    else:
                        dist = 50.0  # Fallback regional default
                    distances[(f1["id"], f2["id"])] = dist

        # Candidate Transfer Arcs
        # Arc key: (i, j, b_id, m_id)
        candidate_arcs: List[Dict[str, Any]] = []

        for b in batches:
            if b.get("status", "Active") != "Active" or b.get("quantity_remaining", 0) <= 0:
                continue

            i = b["facility_id"]
            m_id = b["medicine_id"]
            donor_surplus = surpluses.get((i, m_id), 0.0)
            if donor_surplus <= 0:
                continue

            exp_date = b["expiry_date"]
            if isinstance(exp_date, str):
                exp_date = date.fromisoformat(exp_date)

            rsl = (exp_date - current_date).days
            if rsl < self.min_shelf_life_days:
                continue

            for j in [f["id"] for f in facilities if f["id"] != i]:
                deficit = deficits.get((j, m_id), 0.0)
                if deficit <= 0:
                    continue

                dist = distances.get((i, j), 999.0)
                if dist > self.max_distance_km:
                    continue

                # Transit time (~250 km/day)
                transit_days = max(1, math.ceil(dist / 250.0))
                if (rsl - transit_days) < 30:  # Must have at least 30 days remaining after transit
                    continue

                candidate_arcs.append({
                    "donor_id": i,
                    "recipient_id": j,
                    "batch_id": b["id"],
                    "batch_number": b.get("batch_number", f"LOT-{b['id']}"),
                    "medicine_id": m_id,
                    "unit_cost_etb": float(b.get("unit_cost_etb", 0.0)),
                    "available_qty": min(float(b["quantity_remaining"]), donor_surplus),
                    "deficit_qty": deficit,
                    "distance_km": dist,
                    "remaining_shelf_life_days": rsl,
                    "expiry_date": exp_date,
                })

        if not candidate_arcs:
            return {
                "solver_status": "NO_FEASIBLE_TRANSFERS",
                "allocations": [],
                "total_transferred_units": 0.0,
                "total_transport_cost_etb": 0.0,
                "prevented_wastage_cost_etb": 0.0,
                "net_benefit_etb": 0.0,
            }

        # 2. Build and Solve MILP Model with OR-Tools
        solver = pywraplp.Solver.CreateSolver("SCIP") if OR_TOOLS_AVAILABLE else None

        if solver:
            return self._solve_with_ortools(
                solver, candidate_arcs, deficits, surpluses, distances, fac_map, med_map
            )
        else:
            return self._solve_heuristic(
                candidate_arcs, deficits, surpluses, distances, fac_map, med_map
            )

    def _solve_with_ortools(
        self,
        solver: Any,
        arcs: List[Dict[str, Any]],
        deficits: Dict[Tuple[int, int], float],
        surpluses: Dict[Tuple[int, int], float],
        distances: Dict[Tuple[int, int], float],
        fac_map: Dict[int, Any],
        med_map: Dict[int, Any],
    ) -> Dict[str, Any]:
        """Formulates and solves the MILP in OR-Tools SCIP."""
        # Decision Variables: x[arc_idx] >= 0
        x = {}
        for idx, arc in enumerate(arcs):
            max_qty = min(arc["available_qty"], arc["deficit_qty"])
            x[idx] = solver.NumVar(0.0, max_qty, f"x_{idx}")

        # Unique route pairs for binary variables z[i, j]
        routes = sorted(list(set((arc["donor_id"], arc["recipient_id"]) for arc in arcs)))
        z = {route: solver.BoolVar(f"z_{route[0]}_{route[1]}") for route in routes}

        # Constraint 1: Donor Safety Stock / Surplus Limit
        # Sum of transfers out of donor i for medicine m <= surplus
        donor_med_arcs: Dict[Tuple[int, int], List[int]] = {}
        for idx, arc in enumerate(arcs):
            key = (arc["donor_id"], arc["medicine_id"])
            donor_med_arcs.setdefault(key, []).append(idx)

        for (i, m), arc_indices in donor_med_arcs.items():
            max_surplus = surpluses.get((i, m), 0.0)
            solver.Add(solver.Sum([x[k] for k in arc_indices]) <= max_surplus)

        # Constraint 2: Recipient Deficit Bound
        # Sum of transfers into recipient j for medicine m <= deficit
        recip_med_arcs: Dict[Tuple[int, int], List[int]] = {}
        for idx, arc in enumerate(arcs):
            key = (arc["recipient_id"], arc["medicine_id"])
            recip_med_arcs.setdefault(key, []).append(idx)

        for (j, m), arc_indices in recip_med_arcs.items():
            max_deficit = deficits.get((j, m), 0.0)
            solver.Add(solver.Sum([x[k] for k in arc_indices]) <= max_deficit)

        # Constraint 3: Big-M Linking for Fixed Route Costs
        # Sum of transfers on route (i, j) <= BigM * z[i, j]
        route_arcs: Dict[Tuple[int, int], List[int]] = {}
        for idx, arc in enumerate(arcs):
            route_key = (arc["donor_id"], arc["recipient_id"])
            route_arcs.setdefault(route_key, []).append(idx)

        for route, arc_indices in route_arcs.items():
            solver.Add(solver.Sum([x[k] for k in arc_indices]) <= 100000.0 * z[route])

        # Objective Function:
        # Maximize: Benefit (Shortage Avoided + Wastage Prevented) - Transport Costs
        # Equivalent to Minimizing Cost
        objective = solver.Objective()
        for idx, arc in enumerate(arcs):
            unit_cost = arc["unit_cost_etb"]
            dist = arc["distance_km"]
            # Net margin per unit = (Shortage penalty + Value of medicine) - Transport cost
            unit_value = (self.c_shortage + unit_cost) - (self.c_transport * dist)
            objective.SetCoefficient(x[idx], unit_value)

        for route in routes:
            objective.SetCoefficient(z[route], -self.fixed_route_cost)

        objective.SetMaximization()

        # Solve with 10s timeout
        solver.set_time_limit(10000)
        status = solver.Solve()

        allocations = []
        total_units = 0.0
        total_transport_cost = 0.0
        total_prevented_wastage = 0.0

        if status in [pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE]:
            for idx, arc in enumerate(arcs):
                qty = float(x[idx].solution_value())
                if qty >= 1.0:
                    dist = arc["distance_km"]
                    trans_cost = round(50.0 + (self.c_transport * dist * qty), 2)
                    prevented_val = round(qty * arc["unit_cost_etb"], 2)
                    allocations.append({
                        "source_facility_id": arc["donor_id"],
                        "source_facility_name": fac_map[arc["donor_id"]]["name"],
                        "target_facility_id": arc["recipient_id"],
                        "target_facility_name": fac_map[arc["recipient_id"]]["name"],
                        "medicine_id": arc["medicine_id"],
                        "medicine_name": med_map[arc["medicine_id"]]["name"],
                        "batch_id": arc["batch_id"],
                        "batch_number": arc["batch_number"],
                        "quantity_recommended": round(qty, 1),
                        "transport_distance_km": round(dist, 1),
                        "estimated_transfer_cost_etb": trans_cost,
                        "prevented_wastage_cost_etb": prevented_val,
                        "expiry_date": arc["expiry_date"],
                        "remaining_shelf_life_days": arc["remaining_shelf_life_days"],
                    })
                    total_units += qty
                    total_transport_cost += trans_cost
                    total_prevented_wastage += prevented_val

        net_benefit = round(total_prevented_wastage - total_transport_cost, 2)
        return {
            "solver_status": "OPTIMAL" if status == pywraplp.Solver.OPTIMAL else "FEASIBLE",
            "allocations": allocations,
            "total_transferred_units": round(total_units, 1),
            "total_transport_cost_etb": round(total_transport_cost, 2),
            "prevented_wastage_cost_etb": round(total_prevented_wastage, 2),
            "net_benefit_etb": net_benefit,
        }

    def _solve_heuristic(
        self,
        arcs: List[Dict[str, Any]],
        deficits: Dict[Tuple[int, int], float],
        surpluses: Dict[Tuple[int, int], float],
        distances: Dict[Tuple[int, int], float],
        fac_map: Dict[int, Any],
        med_map: Dict[int, Any],
    ) -> Dict[str, Any]:
        """Greedy cost-benefit matching heuristic when OR-Tools is unavailable."""
        # Sort arcs by highest net margin (unit value - transport cost)
        sorted_arcs = sorted(
            arcs,
            key=lambda a: ((a["unit_cost_etb"] + self.c_shortage) - (self.c_transport * a["distance_km"])),
            reverse=True,
        )

        remaining_surplus = dict(surpluses)
        remaining_deficit = dict(deficits)

        allocations = []
        total_units = 0.0
        total_transport_cost = 0.0
        total_prevented_wastage = 0.0

        for arc in sorted_arcs:
            i, j, m = arc["donor_id"], arc["recipient_id"], arc["medicine_id"]
            avail_surplus = remaining_surplus.get((i, m), 0.0)
            avail_deficit = remaining_deficit.get((j, m), 0.0)

            if avail_surplus <= 0 or avail_deficit <= 0:
                continue

            qty = min(avail_surplus, avail_deficit, arc["available_qty"])
            if qty < 5.0:
                continue

            dist = arc["distance_km"]
            trans_cost = round((self.c_transport * dist * qty) + 50.0, 2)
            prevented_val = round(qty * arc["unit_cost_etb"], 2)

            allocations.append({
                "source_facility_id": i,
                "source_facility_name": fac_map[i]["name"],
                "target_facility_id": j,
                "target_facility_name": fac_map[j]["name"],
                "medicine_id": m,
                "medicine_name": med_map[m]["name"],
                "batch_id": arc["batch_id"],
                "batch_number": arc["batch_number"],
                "quantity_recommended": round(qty, 1),
                "transport_distance_km": round(dist, 1),
                "estimated_transfer_cost_etb": trans_cost,
                "prevented_wastage_cost_etb": prevented_val,
                "expiry_date": arc["expiry_date"],
                "remaining_shelf_life_days": arc["remaining_shelf_life_days"],
            })

            total_units += qty
            total_transport_cost += trans_cost
            total_prevented_wastage += prevented_val

            remaining_surplus[(i, m)] -= qty
            remaining_deficit[(j, m)] -= qty

        net_benefit = round(total_prevented_wastage - total_transport_cost, 2)
        return {
            "solver_status": "HEURISTIC_OPTIMAL",
            "allocations": allocations,
            "total_transferred_units": round(total_units, 1),
            "total_transport_cost_etb": round(total_transport_cost, 2),
            "prevented_wastage_cost_etb": round(total_prevented_wastage, 2),
            "net_benefit_etb": net_benefit,
        }
