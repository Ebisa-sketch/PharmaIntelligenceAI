# Inter-Facility Redistribution Optimization Methodology

---

## 1. Problem Overview and Mathematical Formulation

When health facilities in a regional cluster operate in isolation, geographic supply-demand imbalances emerge: some clinics face acute stockouts of life-saving medicines while neighboring facilities hold excess batches nearing expiry.

PharmaIntelligence AI formulates lateral stock redistribution as a **Mixed-Integer Linear Programming (MILP)** optimization problem solved using the **Google OR-Tools** mathematical optimization suite.

---

## 2. Mathematical Model Formulation

### 2.1 Sets and Indices
- $i, j \in \mathcal{F}$: Set of healthcare facilities within the regional network ($i = \text{donor}$, $j = \text{recipient}$).
- $m \in \mathcal{M}$: Set of pharmaceutical commodities.
- $b \in \mathcal{B}_{i,m}$: Set of active inventory batches of medicine $m$ located at facility $i$.

### 2.2 Parameters
- $S_{ibm}$: Current stock quantity of batch $b$ of medicine $m$ at facility $i$.
- $\text{PUSE}_{ibm}$: Projected Unused Stock at Expiry for batch $b$ at facility $i$.
- $SS_{im}$: Minimum safety stock buffer required at donor facility $i$ (e.g., 30 days of projected demand).
- $D_{jm}$: Projected unmet demand / shortage deficit at recipient facility $j$ over the planning horizon.
- $d_{ij}$: Geographic road transit distance (km) between facility $i$ and facility $j$.
- $T_{ij}$: Estimated road transit time in days.
- $RSL_{b}$: Remaining shelf life of batch $b$ in days.
- $C_{\text{shortage}}$: Unit penalty cost for unfulfilled medicine shortage at recipient.
- $C_{\text{waste}}$: Unit penalty cost for expired medicine wastage.
- $C_{\text{transport}}$: Transportation cost per kilometer per unit transferred.
- $D_{\max}$: Maximum allowable lateral transit distance (e.g., 75 km).
- $CC_m$: Binary indicator; $1$ if medicine $m$ requires cold chain (2–8°C).
- $FC_j$: Binary indicator; $1$ if facility $j$ possesses functional cold chain storage.

### 2.3 Decision Variables
- $x_{ijbm} \ge 0$: Continuous (or integer) quantity of batch $b$ of medicine $m$ transferred from donor facility $i$ to recipient $j$.
- $u_{jm} \ge 0$: Residual unmet demand of medicine $m$ at recipient $j$ post-optimization.
- $w_{ibm} \ge 0$: Residual expired waste of batch $b$ at donor $i$ post-optimization.
- $z_{ij} \in \{0, 1\}$: Binary indicator equal to $1$ if any stock transfer occurs along route $(i, j)$ (to model fixed route dispatch costs).

---

## 3. Objective Function

The objective is to minimize the total system cost, balancing shortage penalties, expiry wastage costs, and physical transport expenditures:

$$\min \sum_{j \in \mathcal{F}} \sum_{m \in \mathcal{M}} C_{\text{shortage}} \cdot u_{jm} + \sum_{i \in \mathcal{F}} \sum_{m \in \mathcal{M}} \sum_{b \in \mathcal{B}_{i,m}} C_{\text{waste}} \cdot w_{ibm} + \sum_{i \in \mathcal{F}} \sum_{j \in \mathcal{F}} \left( F_{ij} \cdot z_{ij} + \sum_{m \in \mathcal{M}} \sum_{b \in \mathcal{B}_{i,m}} C_{\text{transport}} \cdot d_{ij} \cdot x_{ijbm} \right)$$

---

## 4. Operational and Clinical Constraints

### 4.1 Donor Safety Stock Protection (Hard Constraint)
Transfers from donor facility $i$ must NEVER breach its local safety stock requirement $SS_{im}$:
$$\sum_{j \ne i} \sum_{b \in \mathcal{B}_{i,m}} x_{ijbm} \le \max\left(0, \sum_{b \in \mathcal{B}_{i,m}} S_{ibm} - SS_{im}\right), \quad \forall i, m$$

### 4.2 Batch Availability Bound
Total transfers of batch $b$ cannot exceed its current on-hand quantity:
$$\sum_{j \ne i} x_{ijbm} \le S_{ibm}, \quad \forall i, m, b \in \mathcal{B}_{i,m}$$

### 4.3 Recipient Deficit Absorption Bound
A recipient facility cannot be allocated more stock than its projected shortage:
$$\sum_{i \ne j} \sum_{b} x_{ijbm} \le D_{jm}, \quad \forall j, m$$

### 4.4 Shelf-Life Viability Constraint
Transferred batches must have sufficient remaining shelf life to survive transit time $T_{ij}$ plus the recipient's consumption duration:
$$x_{ijbm} \cdot \left( RSL_b - T_{ij} - \frac{x_{ijbm}}{\hat{d}_{jm}} \right) \ge 0, \quad \forall i, j, b, m$$
Batches failing this condition are excluded a priori from decision variable initialization ($x_{ijbm} = 0$).

### 4.5 Distance and Cold-Chain Feasibility
- Geographic threshold: $x_{ijbm} = 0$ if $d_{ij} > D_{\max}$.
- Cold-chain compatibility: $x_{ijbm} = 0$ if $CC_m = 1$ and $FC_j = 0$.

---

## 5. Solver Implementation in OR-Tools

The model is implemented in Python using the `ortools.linear_solver.pywraplp` module using the **SCIP (Solving Constraint Integer Programs)** or **CBC** backend:
1. **Variable Declaration:** Fast continuous/integer variable registration with bounds.
2. **Constraint Formulation:** Vectorized constraint generation via list comprehensions.
3. **Execution & Timeouts:** Solver execution is capped at 10 seconds per cluster run; if the optimal solution is not found within 10 seconds, the best feasible integer solution is returned.
4. **Output Packaging:** Solution translates into structured Pydantic recommendation models with detailed impact statistics.
