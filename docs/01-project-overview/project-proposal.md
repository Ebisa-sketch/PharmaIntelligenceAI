# Project Proposal: PharmaIntelligence AI

## An Explainable AI-Based Decision-Support System for Pharmaceutical Stockout Risk, Expiry Prevention, and Inventory Redistribution in Ethiopian Healthcare Facilities

---

### Executive Summary

PharmaIntelligence AI is an applied artificial intelligence, data engineering, and full-stack software system designed to mitigate two interlocking failures in pharmaceutical supply chains: **preventable stockouts of essential medicines** and **avoidable wastage due to batch expiration**. Focused specifically on resource-constrained environments—with an initial research and deployment target of Ethiopian public health facilities—the platform provides intelligent decision-support rather than autonomous control.

By synthesizing inventory transaction records, supply lead times, consumption trends, and batch shelf-life metrics, PharmaIntelligence AI equips pharmacy managers, hospital administrators, and regional supply chain directors with predictive visibility and actionable recommendations. The platform is designed around five core intelligence pillars:
1. **Data Quality Intelligence (DQI):** Automated profiling, reconciliation validation, and anomaly detection to identify corrupt or incomplete logistics records before downstream processing.
2. **Demand Forecasting:** Multi-model comparative forecasting (statistical baselines, intermittent demand models, and machine learning) that accounts for stockout-censored historical consumption.
3. **Stockout Risk Intelligence:** Calibrated probabilistic risk estimation determining the likelihood and expected timing of stock exhaustion prior to replenishment.
4. **Expiry Risk Intelligence:** First-Expired-First-Out (FEFO) simulation coupled with projected consumption to identify batch-level wastage risks months before expiration.
5. **Redistribution Optimization:** Constrained Mixed-Integer Linear Programming (MILP) to recommend inter-facility transfers from surplus facilities to stockout-threatened clinics while honoring distance, shelf-life, and minimum reserve rules.

Crucially, every prediction and recommendation is paired with Explainable AI (XAI) diagnostics, model confidence boundaries, and data provenance, maintaining the human-in-the-loop governance required in healthcare operations.

---

### Background & Context

In Ethiopia, pharmaceutical procurement and distribution are primarily coordinated through the Ethiopian Pharmaceuticals Supply Service (EPSS), supplying essential health commodities to regional hubs, referral hospitals, primary hospitals, and health centers. Operational tools such as **Dagu** (an electronic Logistics Management Information System, eLMIS) and national quantification frameworks like **ForLab+** have vastly improved visibility over paper-based records.

However, health facilities continue to experience recurring operational frictions:
- **Data Quality Inconsistencies:** Discrepancies between physical bin cards and digital records, missed entries, delayed reporting, and manual data-entry errors undermine analytical reliability.
- **Intermittent & Censored Consumption:** Medicine consumption is frequently sporadic. Furthermore, recorded consumption plummets during stockouts not because patient demand vanished, but because no physical medicine was available to dispense ("censored demand").
- **Unpredictable Supply Lead Times:** Lead times from central and regional hubs vary widely due to import constraints, foreign exchange availability, and transportation bottlenecks.
- **Stock Imbalances Across Neighboring Facilities:** It is common for one district hospital to suffer a stockout of antibiotics or insulin while a neighboring facility holds surplus batches nearing expiry without an automated mechanism to identify or approve lateral transfers.

---

### Proposed Solution

PharmaIntelligence AI does not seek to replace national logistics information systems such as Dagu or ForLab+, nor does it assume continuous network connectivity or proprietary backend database access. Instead, it introduces an **explainable analytical and decision-support layer** capable of operating on standardized, authorized data imports (CSV, Excel, or future FHIR/LMIS API feeds).

```
┌────────────────────────────────────────────────────────┐
│                   PharmaIntelligence AI                │
├────────────────────────────────────────────────────────┤
│  1. Data Quality Intelligence (Validation & Profiling) │
│  2. Censoring-Aware Medicine Demand Forecasting        │
│  3. Multi-Horizon Stockout Risk Classification         │
│  4. Batch-Level FEFO Expiry Risk Evaluation            │
│  5. Constrained Inter-Facility Redistribution Engine   │
│  6. Human-in-the-Loop Explainability & Audit Trail     │
└────────────────────────────────────────────────────────┘
```

---

### Key Capabilities & Architectural Scope

| Capability | Technical Mechanism | Primary Output |
|---|---|---|
| **Data Cleaning & Audit** | Pydantic validation schemas, statistical IQR checks, stock reconciliation balance checks | Data Quality Score, transaction reconciliation warnings |
| **Demand Forecasting** | Naive, Seasonal Naive, Moving Average, Croston, TSB, LightGBM, XGBoost, Prophet | Point forecasts, 80%/95% prediction intervals |
| **Stockout Risk Modeling** | Days of Stock Remaining (DSR), lead-time buffer analysis, Logistic Regression / Random Forest classifiers | Stockout Probability (0–100%), Priority Category (Critical/Warning/Safe) |
| **Expiry Waste Prediction** | Deterministic FEFO depletion timeline against demand curve, batch shelf-life tracking | Projected Unused Quantity, Financial Value at Risk, Days to Expire |
| **Redistribution Engine** | Google OR-Tools / Pyomo MILP optimization engine | Ranked transfer proposals (Donor, Recipient, Batch, Qty, Distance, Savings) |
| **Transparency & XAI** | TreeSHAP, Waterfall plots, transparent decision rules, confidence flags | Factor contribution breakdown, model versioning tags |

---

### Target Beneficiaries & Operational Roles

- **Facility Pharmacy Managers:** Immediate alerts on critical stockouts, prioritized batch dispensing schedules, and review of incoming/outgoing lateral transfer requests.
- **Hospital Chief Pharmacists & CEOs:** Consolidated facility risk posture, inventory valuation at risk of expiry, and automated audit logs.
- **Regional Health Bureau (RHB) / EPSS Hub Officers:** Cross-facility visibility across district networks to approve or coordinate lateral stock transfers before submitting emergency purchase orders.
- **Supply Chain Researchers & Analysts:** A standardized sandbox to benchmark forecasting algorithms against real or synthetic Ethiopian public health datasets.

---

### Project Phasing and Milestones

1. **Phase 1: Research, Requirements & Dataset Acquisition (Weeks 1–4)**  
   Systematic literature review, empirical gap analysis, data governance protocols, synthetic benchmark dataset generation.
2. **Phase 2: Core Data Engineering & Validation Service (Weeks 5–7)**  
   Data ingestion pipelines, Pydantic data contract enforcement, automated reconciliation discrepancy algorithms.
3. **Phase 3: Machine Learning & Predictive Modeling (Weeks 8–12)**  
   Intermittent forecasting pipeline, stockout classifier training, SHAP explainability engine, backtesting harness.
4. **Phase 4: Redistribution Optimization & Simulation Engine (Weeks 13–15)**  
   MILP mathematical formulation in OR-Tools, transfer constraint checks, synthetic simulation of stockout/waste reduction.
5. **Phase 5: Full-Stack Web Platform Development (Weeks 16–19)**  
   FastAPI REST services, PostgreSQL database schema with role-based access control, Next.js frontend with Tailwind CSS and shadcn/ui.
6. **Phase 6: Verification, Performance Testing & Final Reporting (Weeks 20–22)**  
   End-to-end testing, security audits, academic report completion, open-source codebase delivery.
