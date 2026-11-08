# Functional Requirements Specification

This document details the complete functional requirements for PharmaIntelligence AI. Every requirement follows the standard `FR-XX` identifier scheme.

---

## FR-01: Authentication, Authorization, and Session Management
- **FR-01.1:** The system MUST authenticate users via secure email/username and password using Bcrypt/Argon2 password hashing.
- **FR-01.2:** The system MUST issue secure, short-lived JWT access tokens and long-lived refresh tokens with HTTP-only cookies.
- **FR-01.3:** The system MUST enforce Role-Based Access Control (RBAC) at the API and service layers for every protected resource.
- **FR-01.4:** The system MUST restrict facility-level data access such that facility users can only inspect records for their assigned facilities, unless assigned regional or administrator privileges.

---

## FR-02: Facility and Medicine Master Reference Management
- **FR-02.1:** The system MUST maintain master records for healthcare facilities, including unique ID, facility name, tier (Referral Hospital, Primary Hospital, Health Center), geographic coordinates (latitude, longitude), and administrative zone/woreda.
- **FR-02.2:** The system MUST maintain master records for medicines, including unique medicine code, generic name, dosage form, strength, therapeutic category, standard dispensing unit, and storage requirements (ambient, cold chain 2–8°C).
- **FR-02.3:** The system MUST validate incoming records against the master medicine dictionary and flag unmapped or misspelled identifiers.

---

## FR-03: Multi-Source Data Ingestion Pipeline
- **FR-03.1:** The system MUST allow authorized users to upload inventory files in CSV, TSV, and Excel (.xlsx) formats.
- **FR-03.2:** The system MUST validate column presence, data types, date formatting, and numerical constraints upon upload.
- **FR-03.3:** The system MUST preserve full import provenance: upload timestamp, uploading user ID, original file checksum (SHA-256), and raw record counts.
- **FR-03.4:** The system MUST provide an interactive row-level error log for rejected records with explicit rejection reasons (e.g., negative quantity, invalid date).
- **FR-03.5:** Re-importing identical files MUST be idempotent and prevent duplicate transaction entries.

---

## FR-04: Data Quality Intelligence (DQI) Engine
- **FR-04.1:** The system MUST calculate a facility-level Data Quality Completeness Index (DQCI) assessing missingness, anomalies, and reconciliation integrity.
- **FR-04.2:** The system MUST perform inventory reconciliation checks where opening, closing, receipt, issue, and adjustment transactions exist:
  $$\Delta = \text{Closing} - (\text{Opening} + \text{Receipts} - \text{Issues} + \text{Adjustments})$$
- **FR-04.3:** The system MUST flag transaction anomalies using statistical outlier boundaries (IQR > 3.0) and Isolation Forest algorithms.
- **FR-04.4:** The system MUST persist detected data-quality issues in a dedicated `data_quality_issues` table without modifying raw source rows.

---

## FR-05: Real-Time Inventory & Batch Tracking
- **FR-05.1:** The system MUST display current usable stock, reserved stock, and quarantine stock per medicine and facility.
- **FR-05.2:** The system MUST track batch-level metadata: batch number, manufacture date, expiry date, initial quantity, current remaining quantity, and batch status.
- **FR-05.3:** The system MUST enforce First-Expired-First-Out (FEFO) prioritization in all batch consumption calculations.

---

## FR-06: Medicine Demand Forecasting Engine
- **FR-06.1:** The system MUST generate demand forecasts across configurable horizons (1 to 6 months forward).
- **FR-06.2:** The system MUST support multiple forecasting models: Naive, Moving Average, Seasonal Naive, Croston, TSB, LightGBM, and XGBoost.
- **FR-06.3:** The system MUST provide stockout-censoring adjustments by scaling observed consumption by the proportion of in-stock operating days.
- **FR-06.4:** The system MUST produce uncertainty bounds (e.g., 80% and 95% prediction intervals) for supported models.
- **FR-06.5:** The system MUST display comparative historical evaluation metrics (MASE, WAPE, RMSE) against baseline models for each medicine.

---

## FR-07: Stockout Risk Intelligence
- **FR-07.1:** The system MUST calculate current Days of Stock Remaining (DSR):
  $$\text{DSR} = \frac{\text{Current Usable Stock}}{\text{Projected Daily Demand}}$$
- **FR-07.2:** The system MUST classify stockout risk into standardized priority tiers: **Critical** (< 14 days), **High** (14–30 days), **Moderate** (31–60 days), **Safe** (> 60 days).
- **FR-07.3:** The system MUST incorporate open requisition orders and supplier lead-time distributions into stockout risk probability estimation.
- **FR-07.4:** The system MUST explicitly display a "Data Insufficient" warning when essential lead-time or demand features are missing.

---

## FR-08: Batch Expiry Risk Intelligence
- **FR-08.1:** The system MUST calculate Remaining Shelf Life (RSL) in days for all active batches.
- **FR-08.2:** The system MUST project cumulative demand over the batch's remaining life using FEFO allocation.
- **FR-08.3:** The system MUST calculate Projected Unused Quantity at Expiry (PUSE) and estimated financial value at risk.
- **FR-08.4:** The system MUST categorize batches into Expiry Tiers: Critical (< 60 days to expiry with projected surplus), Warning (61–180 days with projected surplus), and Normal.

---

## FR-09: Lateral Redistribution Optimization Engine
- **FR-09.1:** The system MUST identify donor facilities holding verified surplus and recipient facilities facing stockouts within the same regional cluster.
- **FR-09.2:** The optimization solver MUST enforce hard constraints:
  - Donor facility MUST retain a minimum safety buffer (e.g., 30 days of projected demand).
  - Transferred batches MUST arrive with sufficient shelf-life to cover recipient consumption time + minimum margin.
  - Maximum geographic transit distance / duration constraints.
  - Cold-chain compatibility between donor and recipient.
- **FR-09.3:** The system MUST generate prioritized, ranked transfer recommendations specifying: Donor, Recipient, Medicine, Batch ID, Quantity, Estimated Transport Distance, and Avoided Waste / Stockout Impact.
- **FR-09.4:** The system MUST provide an interactive human review workflow where authorized users can **Accept**, **Modify Quantity**, or **Reject** recommendations with mandatory justification notes.
- **FR-09.5:** Rejected or approved transfers MUST NOT trigger automatic physical shipments.

---

## FR-10: Explainable AI (XAI) & Decision Transparency
- **FR-10.1:** The system MUST display top-5 contributing features for machine-learning-derived predictions using TreeSHAP or localized attribution.
- **FR-10.2:** The system MUST generate plain-language explanations summarizing model findings (e.g., *"Elevated stockout risk driven by a 40% surge in pediatric cases and a 20-day delivery delay from EPSS hub"*).
- **FR-10.3:** The system MUST display model metadata alongside predictions: model type, training dataset version, and timestamp.

---

## FR-11: Reporting and Data Export
- **FR-11.1:** The system MUST allow authorized users to generate and export inventory summary, stockout risk, expiry warning, and redistribution reports in CSV and PDF formats.
- **FR-11.2:** Exported documents MUST include data generation timestamps, active user credentials, and confidentiality notices.

---

## FR-12: Audit Logging and System Provenance
- **FR-12.1:** The system MUST record immutable audit log entries for all significant user actions: login attempts, data uploads, recommendation approvals, rejections, and user permission changes.
- **FR-12.2:** Each audit record MUST capture: timestamp (UTC), user ID, user IP address, target entity type, action type, and JSON payload of state changes.
- **FR-12.3:** Audit logs MUST be protected from modification or deletion via administrative UI.
