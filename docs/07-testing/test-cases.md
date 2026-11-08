# Test Cases Specification

---

## 1. Test Case Catalog Overview

This document specifies the core functional and boundary test cases across authentication, data quality intelligence, forecasting, risk scoring, and redistribution optimization.

---

## 2. Detailed Test Cases

### TC-AUTH: Authentication & Access Control

#### `TC-AUTH-001`: Valid Login and JWT Generation
- **Type:** Unit / Integration
- **Preconditions:** User `manager@hospital.gov.et` exists with role `ROLE_PHARMACY_MANAGER`.
- **Input:** `POST /api/v1/auth/login` with correct password.
- **Expected Result:** HTTP 200 OK, response returns valid access token with `exp` timestamp and user facility scope.
- **Pass/Fail Criteria:** JWT payload decodes with correct `sub` and `role`.

#### `TC-AUTH-002`: Cross-Facility Unauthorized Data Access
- **Type:** Security / Integration
- **Preconditions:** User is assigned to `facility_id: FAC-001`.
- **Input:** `GET /api/v1/inventory/batches?facility_id=FAC-002`.
- **Expected Result:** HTTP 403 Forbidden.
- **Pass/Fail Criteria:** Access is rejected; security event is logged in `audit_logs`.

---

### TC-DQI: Data Quality Intelligence

#### `TC-DQI-001`: Transaction Ledger Reconciliation Mismatch
- **Type:** Unit
- **Input Row:** $\text{Opening} = 100$, $\text{Receipts} = 50$, $\text{Issues} = 30$, $\text{Adjustments} = 0$, $\text{Actual Closing} = 110$.
- **Calculation:** Expected Closing = $100 + 50 - 30 = 120$. Discrepancy $\Delta = -10$.
- **Expected Result:** System creates entry in `data_quality_issues` with `issue_type: RECONCILIATION_ERROR`, severity `WARNING`.
- **Pass/Fail Criteria:** Row is flagged; discrepancy quantity $(-10)$ captured in issue details JSON.

#### `TC-DQI-002`: Re-import Idempotency and Deduplication
- **Type:** Integration
- **Input:** Upload identical `inventory_oct_2026.csv` file twice within 5 minutes.
- **Expected Result:** First upload processes 1,000 rows. Second upload detects identical SHA-256 file checksum and returns HTTP 409 Conflict or a warning message without creating duplicate ledger records.
- **Pass/Fail Criteria:** Total database row count remains exactly 1,000.

---

### TC-FC: Demand Forecasting Engine

#### `TC-FC-001`: In-Stock De-censoring Adjustment
- **Type:** Unit
- **Input:** Month with 30 calendar days. Facility had 10 stockout days (20 in-stock days). Observed consumption $C_{\text{obs}} = 400$ units.
- **Calculation:** $R = 20 / 30 \approx 0.667$. $C_{\text{adj}} = 400 / 0.667 = 600$ units.
- **Expected Result:** De-censored feature matrix reflects $600$ units for that period.
- **Pass/Fail Criteria:** $C_{\text{adj}} == 600.0 \pm 0.01$.

#### `TC-FC-002`: Non-Negative Forecast Output Guarantee
- **Type:** Property-Based / Unit
- **Input:** Random variations of historical time-series containing extended zero sequences.
- **Expected Result:** For all forecasting models (LightGBM, Croston, TSB, Naive), $\hat{y}_{t+h} \ge 0.0$.
- **Pass/Fail Criteria:** Zero occurrences of negative forecast predictions.

---

### TC-OPT: Lateral Redistribution Optimization

#### `TC-OPT-001`: Hard Donor Safety Stock Conservation
- **Type:** Mathematical Solver Verification
- **Scenario:**
  - Donor Facility A holds 500 units of *Ceftriaxone 1g*. Minimum safety stock $SS_A = 200$ units.
  - Recipient Facility B faces an acute deficit of 600 units.
- **Solver Run:** Run MILP redistribution optimization.
- **Expected Result:** Recommended transfer quantity from Facility A to B is strictly $\le 300$ units ($500 - 200$).
- **Pass/Fail Criteria:** Donor stock post-transfer is $\ge 200$ units; transfer quantity is exactly 300 units.

#### `TC-OPT-002`: Expired Batch Transit Rejection
- **Type:** Constraint Boundary Test
- **Scenario:** Batch expiring in 5 days. Estimated road transit time is 3 days, plus recipient minimum absorption time is 7 days ($5 < 3 + 7$).
- **Expected Result:** Optimization solver assigns $x_{ijbm} = 0$; batch is excluded from redistribution proposals.
- **Pass/Fail Criteria:** Short-dated batch is never recommended for inter-facility dispatch.
