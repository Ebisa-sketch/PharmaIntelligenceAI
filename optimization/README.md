# PharmaIntelligence AI - Supply Chain Optimization Framework

This directory contains the mathematical programming models, solvers, scenario generators, and evaluation simulators for pharmaceutical inventory allocation, replenishment, and network distribution.

## Architecture Overview

```
optimization/
├── models/             # Mathematical modeling formulations (variables, objectives, constraints)
│   ├── decision_variables.py
│   ├── objective_functions.py
│   └── constraints.py
├── solvers/            # Multi-backend solver integrations (Google OR-Tools, Pyomo)
│   ├── ortools_solver.py
│   └── pyomo_solver.py
├── scenarios/          # Stress-test scenario generators (epidemic surge, disruption, expiry decay)
│   ├── shortage_scenarios.py
│   ├── expiry_scenarios.py
│   └── transport_scenarios.py
├── evaluation/         # Simulation and benchmark comparison against baseline policies
│   ├── simulation.py
│   └── comparison.py
└── README.md
```

## Core Components

### 1. Mathematical Formulations (`optimization/models/`)
- **`decision_variables.py`**: Defines decision spaces for replenishment orders, multi-echelon warehouse transshipments, inventory tracking, unmet demand shortages, and expired batch disposals.
- **`objective_functions.py`**: Cost minimization formulations balancing holding costs, shortage penalties (weighted by medical criticality), transportation tariffs, disposal fees, and fixed order overhead.
- **`constraints.py`**: Rigorous multi-period flow balance, storage volume capacities, and cold-chain compliance limits.

### 2. Solver Interfaces (`optimization/solvers/`)
- **`ortools_solver.py`**: Google OR-Tools interface utilizing high-performance linear and integer solvers (CBC, SCIP, GLOP).
- **`pyomo_solver.py`**: Pyomo algebraic modeling system integration with extensible dispatch to GLPK, Gurobi, CPLEX, and HiGHS.

### 3. Scenario Analysis (`optimization/scenarios/`)
- **`shortage_scenarios.py`**: Epidemic demand surges and upstream API supplier manufacturing outages.
- **`expiry_scenarios.py`**: Shelf-life deterioration from cold-chain temperature excursion incidents.
- **`transport_scenarios.py`**: Freight corridor blockages and transit delay propagation.

### 4. Policy Benchmarking (`optimization/evaluation/`)
- **`simulation.py`**: Rolling-horizon discrete simulation evaluating policy robustness under realized stochastic demand.
- **`comparison.py`**: Head-to-head benchmarking comparing MILP optimized decisions against classic inventory rules like `(s, S)`, Economic Order Quantity (EOQ), and periodic review baselines.
