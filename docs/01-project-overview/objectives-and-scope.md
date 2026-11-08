# Project Objectives and System Scope

---

## 1. General Objective

To design, develop, and evaluate an explainable, uncertainty-aware artificial intelligence decision-support platform for pharmaceutical inventory management, specifically targeted at reducing stockout occurrences, mitigating avoidable expiry wastage, and enabling optimized lateral inventory redistribution across Ethiopian public healthcare facilities.

---

## 2. Specific Objectives

1. **Systematic Review & Contextual Benchmarking:** Review existing literature on pharmaceutical inventory analytics, eLMIS frameworks (such as Dagu), and quantify specific logistical gaps in the Ethiopian public healthcare supply chain.
2. **Dataset Acquisition & Synthetic Benchmarking:** Identify, curate, and profile real-world or realistic synthetic pharmaceutical supply-chain datasets reflecting multi-facility inventory transactions, lead times, batch metadata, and stockout histories.
3. **Data Quality Intelligence (DQI) Engine:** Formulate automated data validation and reconciliation algorithms capable of detecting missing, duplicated, conflicting, anomalous, and mathematically impossible inventory balance transactions.
4. **Censoring-Aware Demand Forecasting:** Develop and evaluate statistical baselines (Naive, Moving Average, Seasonal Naive, Croston, TSB) and machine-learning models (LightGBM, XGBoost) incorporating demand de-censoring techniques.
5. **Multi-Horizon Stockout Risk Intelligence:** Engineer a probabilistic classification and survival-analysis framework to project the likelihood and estimated timing of stock depletion ahead of replenishment.
6. **Batch-Level Expiry Prevention Analysis:** Build a deterministic and forecast-assisted batch tracking engine applying First-Expired-First-Out (FEFO) rules to identify batches with projected residual waste.
7. **Constrained Redistribution Optimization Engine:** Formulate and solve a Mixed-Integer Linear Program (MILP) utilizing Google OR-Tools / Pyomo to calculate feasible, cost-effective inter-facility stock transfers under clinical, operational, and distance constraints.
8. **Explainable AI (XAI) & Decision Diagnostics:** Integrate model-agnostic and tree-specific explanation techniques (TreeSHAP, feature importance, uncertainty intervals) to provide actionable rationales for all predictions and transfer suggestions.
9. **Secure Full-Stack Web Prototype:** Implement a production-grade web application featuring a Python FastAPI backend, PostgreSQL relational database, and Next.js / TypeScript frontend with role-based access control and comprehensive audit logging.
10. **Empirical Evaluation & Simulation:** Conduct extensive backtesting and discrete-event simulation to evaluate the marginal benefit of AI-assisted decision-support against traditional static inventory management rules.

---

## 3. Project Scope

### 3.1 In-Scope Capabilities
- **Batch & Inventory Records:** Ingestion and processing of stock on hand, bin-card transactions, physical counts, batch numbers, and expiration dates.
- **Data Ingestion via Standard Formats:** Robust parsing, validation, and schema checking of CSV, Excel, and structured JSON data files.
- **Censored Demand Reconstruction:** Flagging historical stockout periods and adjusting baseline demand estimates.
- **Intermittent Time-Series Forecasting:** Time horizons tailored to the operational reporting frequency (monthly, weekly, or daily).
- **Lateral Transfer Recommendations:** Multi-facility transfer planning incorporating transport distance, batch expiry, donor minimum safety stock, and recipient storage requirements.
- **Explainability & Transparency:** Visual and textual explanations of risk factors, forecast confidence bounds, and optimization trade-offs.
- **Human-in-the-Loop Governance:** Strict approval gates for transfer recommendations, audit trails, and data isolation between healthcare facilities.

### 3.2 Out-of-Scope Capabilities
- **Direct Real-Time Integration with National Databases:** The system does not assume live API or direct write access to Ethiopian national databases (e.g., EPSS central ERP, Dagu production databases) without authorized MOUs.
- **Autonomous Supply Chain Execution:** The software will not place binding purchase orders, execute physical courier transfers, or automatically deduct stock without human pharmacist approval.
- **Clinical Prescribing and Diagnostic Advice:** The system does not diagnose medical conditions, recommend patient-specific regimens, or substitute for licensed clinician judgment.
- **Patient Identifiable Data Processing:** No protected health information (PHI) such as patient names, medical record numbers, or personal clinical histories will be captured or stored.
- **Commercial Hardware Procurement:** Design or procurement of specialized warehouse IoT sensor hardware (e.g., RFID tags, temperature-logging hardware) is outside the initial software prototype scope.

---

## 4. Target Pilot Facility Profile

To ground the research and system design in realistic operational parameters, the prototype is targeted to model:
- **Facility Types:** A representative regional cluster comprising 1 Regional Referral Hospital, 2 Primary District Hospitals, and 3–5 Primary Health Centers.
- **Medicine Portfolio:** A representative basket of 15–25 priority essential medicines (antibiotics, anti-malarials, oral hypoglycemics, antihypertensives, maternal health oxytocics).
- **Time Horizon:** Historical records spanning 24 to 36 months of inventory movements, with forecasting horizons evaluating 1 to 6 months forward.
