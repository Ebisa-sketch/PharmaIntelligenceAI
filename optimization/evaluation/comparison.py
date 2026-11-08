"""Benchmark comparison between mathematical optimization policies and heuristic inventory baselines."""

from typing import Dict, List, Any
import pandas as pd


class PolicyComparator:
    """Compares optimization solver outputs against standard replenishment heuristics:
    - (s, S) continuous review policy
    - Fixed order quantity (EOQ)
    - Static safety stock heuristic
    """

    @staticmethod
    def compare_policies(
        baseline_results: Dict[str, Any],
        optimized_results: Dict[str, Any]
    ) -> pd.DataFrame:
        """Constructs benchmark comparison table.

        Args:
            baseline_results: Performance dictionary of standard business heuristic.
            optimized_results: Performance dictionary of MILP solver policy.

        Returns:
            pd.DataFrame comparing service levels, stockouts, expired inventory, and holding costs.
        """
        metrics = ["total_service_level", "total_stockout_events", "total_expired_units", "total_operational_cost"]
        data = {
            "Metric": metrics,
            "Heuristic_Baseline": [baseline_results.get(m, 0.0) for m in metrics],
            "Optimized_MILP": [optimized_results.get(m, 0.0) for m in metrics]
        }
        df = pd.DataFrame(data)
        df["Improvement_Pct"] = (
            (df["Heuristic_Baseline"] - df["Optimized_MILP"]) / df["Heuristic_Baseline"] * 100
        ).round(2)
        return df
