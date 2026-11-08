# Expected Research and Practical Contributions

PharmaIntelligence AI bridges the gap between academic supply chain machine learning and the operational realities of low-resource public healthcare facilities. The expected contributions of this project span theoretical, algorithmic, practical, and open software domains.

---

## 1. Theoretical and Methodological Contributions

### 1.1 Integrated Multi-Pillar Healthcare Supply Chain Framework
Existing literature frequently addresses inventory forecasting, stockout risk, or vehicle routing in isolation. PharmaIntelligence AI presents an integrated, end-to-end conceptual framework linking **Data Quality Assessment $\rightarrow$ De-censored Forecasting $\rightarrow$ Dual Risk Classification (Stockout + Expiry) $\rightarrow$ Lateral Redistribution Optimization $\rightarrow$ Explainable Decision Support**.

### 1.2 De-censoring Methodologies for Low-Resource eLMIS Data
In resource-constrained settings, medicine stockouts create severe right-censoring in consumption logs. This project benchmarks and formalizes practical de-censoring heuristic adjustments (e.g., zero-fill correction, average consumption scaling over in-stock days, Tobit regression baselines) that can be reliably computed without massive computational infrastructure.

### 1.3 Calibrated Multi-Facility Redistribution Optimization Formulation
The project formulates a novel, generalized Mixed-Integer Linear Programming (MILP) model tailored for lateral transfers among public health facilities. Unlike commercial logistics models that prioritize transport cost minimization alone, this formulation incorporates:
- **Shelf-Life Feasibility:** Ensuring batch transit and recipient consumption occur well before expiry.
- **Donor Protection:** Hard constraints preventing donor facilities from breaching minimum safety buffers.
- **Equitable Stock Allocation:** Multi-criteria objective balancing shortage penalties, transport costs, and expiry prevention.

---

## 2. Practical Contributions to Ethiopian Healthcare Logistics

### 2.1 Pragmatic Decision-Support Complement to Dagu & EPSS
Rather than proposing an unfeasible replacement of existing systems, PharmaIntelligence AI provides an **interoperable decision-support sidecar**. It operates cleanly on standard CSV / Excel export formats currently produced by Dagu and health facility reporting templates, enabling immediate utility without requiring nationwide infrastructure overhauls.

### 2.2 Proactive Expiry Mitigation and Budget Preservation
By identifying batch surplus in secondary clinics and matching it to high-consumption referral hospitals 3–6 months prior to expiry, the platform provides healthcare administrators with an actionable tool to safeguard public health funds and reduce pharmaceutical destruction costs.

### 2.3 Transparent Explainability for Clinical and Pharmacy Personnel
Black-box AI creates justified skepticism among healthcare workers. PharmaIntelligence AI delivers transparent, interpretable factor decompositions (via TreeSHAP and rule summaries), explaining *why* a medicine is deemed high-risk and *why* a particular transfer route is recommended.

---

## 3. Software Engineering and Open Science Artifacts

1. **Modular, Production-Ready Open-Source Platform:**
   - **Backend:** High-performance, fully typed Python FastAPI REST services with SQLAlchemy / Pydantic validation.
   - **Frontend:** Responsive Next.js 14 web application built with TypeScript, Tailwind CSS, and shadcn/ui.
   - **Optimization Engine:** Clean, tested Google OR-Tools / Pyomo optimization modules.
2. **Standardized Synthetic Ethiopian Healthcare Supply Chain Benchmark:**
   - A parameterized synthetic data generator capable of producing realistic multi-tier facility records, intermittent consumption patterns, varied supplier lead times, and batch tracking metadata with injection of controlled anomalies.
3. **Reproducible Experimentation Harness:**
   - Standardized Jupyter notebooks and MLflow experiment tracking configurations allowing academic researchers to reproduce all baseline comparisons and metrics.

---

## 4. Summary Contribution Matrix

| Dimension | Conventional System / Current State | PharmaIntelligence AI Contribution |
|---|---|---|
| **Data Quality** | Manual review, undetected reconciliation errors, unflagged anomalies. | Automated structural validation, transaction reconciliation math checks, and anomaly scoring. |
| **Forecasting** | Static moving averages or subjective estimation; ignores stockout-censored demand. | Multi-model benchmarking (Croston, TSB, LightGBM) with stockout de-censoring and prediction intervals. |
| **Stockout Risk** | Static Days-of-Stock threshold; no probabilistic lead time modeling. | Dynamic, probabilistic classification incorporating supply lead-time variance and demand uncertainty. |
| **Expiry Risk** | Passive review of expiring shelf stock; manual bin-card checking. | Forward-looking FEFO simulation projecting exact unused quantities months in advance. |
| **Stock Sharing** | Ad-hoc phone calls between pharmacy heads; reactive emergency transfers. | Mathematical optimization identifying optimal multi-facility transfers subject to strict constraints. |
| **Transparency** | Black-box algorithms or opaque spreadsheets. | Transparent explanations (TreeSHAP), confidence indicators, and human-in-the-loop review. |
