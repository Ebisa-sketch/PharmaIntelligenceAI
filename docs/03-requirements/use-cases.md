# System Use Cases and User Journeys

---

## 1. Overview

This document specifies the primary operational and research use cases for PharmaIntelligence AI, detailing trigger events, actor interactions, preconditions, postconditions, and alternative paths.

---

## 2. Core Use Cases

### UC-01: Ingest and Validate Facility Inventory File
- **Primary Actor:** Facility Pharmacy Manager / Data Analyst
- **Preconditions:** User is authenticated with `data:import` permission for the target facility.
- **Trigger:** Monthly or weekly inventory reconciliation file (CSV/Excel) is ready for upload.
- **Main Flow:**
  1. User navigates to the **Data Quality Center** and selects the target facility.
  2. User drags and drops a CSV transaction file containing opening stock, receipts, issues, adjustments, and closing stock.
  3. System parses the file, checking header schema, date formats, and numerical validity against Pydantic validation rules.
  4. System runs ledger reconciliation checks: $\text{Closing} == \text{Opening} + \text{In} - \text{Out} \pm \text{Adjustments}$.
  5. System computes the Data Quality Score and displays a summary: Total Rows, Valid Rows, Rejected Rows, Reconciliation Warnings.
  6. User reviews error highlights; valid transactions are committed to the database with a unique `import_id`.
- **Alternative Flow:**
  - *Invalid File Format:* System rejects file immediately with specific error message (e.g., "Missing required column: `batch_number`").
  - *Re-import of identical file:* System checks SHA-256 hash, identifies duplicate import, and warns user without duplicating transactions.

---

### UC-02: Review Medicine Demand Forecasts and Explainability
- **Primary Actor:** Facility Pharmacy Manager / Regional Supply Chain Officer
- **Preconditions:** Valid historical consumption records exist for the selected medicine and facility.
- **Main Flow:**
  1. User opens the **Forecasting Center** and selects a medicine (e.g., *Amoxicillin 500mg Capsule*) and facility.
  2. System retrieves historical consumption, applies stockout-censoring corrections, and generates a 3-month forecast using the best-performing model (e.g., LightGBM).
  3. System renders an interactive visualization showing historical consumption, predicted point values, and 80%/95% prediction intervals.
  4. User clicks "Explain Forecast" to open the Explainable AI panel.
  5. System displays a SHAP waterfall plot showing key drivers (e.g., +25% due to seasonal malaria surge, +15% due to expanded pediatric clinic hours).
  6. User exports the forecast summary to PDF for the monthly procurement committee.

---

### UC-03: Assess Stockout and Expiry Risks
- **Primary Actor:** Facility Pharmacy Manager
- **Preconditions:** Inventory records and batch expiry dates are up to date.
- **Main Flow:**
  1. User logs into the **Executive Dashboard**.
  2. System displays priority cards:
     - **Critical Stockouts (< 14 Days):** 3 medicines flagged.
     - **Expiring Batches (< 90 Days):** 2 batches flagged with projected surplus.
  3. User drills into a stockout-threatened medicine (*Metformin 500mg*).
  4. System displays current stock (120 units), projected daily consumption (15 units/day), Days of Stock Remaining (8 days), and pending EPSS delivery (lead time estimate: 21 days $\rightarrow$ High Stockout Probability: 88%).
  5. User marks the item for lateral transfer sourcing.

---

### UC-04: Generate and Review Inter-Facility Redistribution Recommendations
- **Primary Actor:** Regional Supply Chain Officer / Facility Pharmacy Manager
- **Preconditions:** Multiple facilities in a regional cluster have up-to-date inventory data.
- **Main Flow:**
  1. Regional Officer navigates to the **Redistribution Center** and clicks "Run Regional Optimization".
  2. The Google OR-Tools optimization engine solves the MILP problem, balancing surplus batches against stockout needs while respecting transport distance and donor safety stock.
  3. System returns ranked transfer recommendations:
     - *Recommendation #101:* Transfer 300 vials of *Ceftriaxone 1g* from *Debre Berhan Health Center* (Surplus: 450 vials, Expiry: 75 days) to *Debre Berhan Referral Hospital* (Stockout in 6 days).
     - *Distance:* 14 km. *Transport Cost:* Low. *Impact:* Avoids $1,800 USD waste and 22 stockout days.
  4. Regional Officer reviews transfer details, checks cold-chain feasibility, and clicks "Submit for Facility Approval".
  5. Pharmacy Managers at both donor and recipient facilities receive a notification, review the terms, and click "Accept Transfer".
  6. System records the approval in the audit ledger and outputs a standardized physical transfer voucher.
- **Alternative Flow:**
  - *Donor Manager Rejects:* Manager notes that local epidemic requires retaining stock; marks transfer as "Rejected with Reason: Local demand spike". The system recalculates alternative routes.

---

### UC-05: Benchmark ML Models and Run Scientific Experiments
- **Primary Actor:** Data Analyst / Academic Researcher
- **Preconditions:** Researcher role access; benchmark dataset loaded in sandbox environment.
- **Main Flow:**
  1. Researcher navigates to the **AI Model Laboratory**.
  2. Selects dataset version, target medicine category, and cross-validation protocol (Rolling-origin, 6-split backtest).
  3. Selects candidate models (Croston, SBA, LightGBM, XGBoost, ARIMA) and toggles de-censoring on/off.
  4. System executes experiment pipeline asynchronously, recording MASE, WAPE, RMSE, and training runtimes in MLflow.
  5. Researcher views comparative metrics table and downloads publication-ready LaTeX tables and error distribution charts.
