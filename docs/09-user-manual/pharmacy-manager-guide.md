# Facility Pharmacy Manager Guide

## PharmaIntelligence AI — Pharmacy Manager Manual

> **Document status:** Draft  
> **Last updated:** 2026-11-05

---

## 1. Overview

This guide is for **Facility Pharmacy Managers** who use PharmaIntelligence AI to monitor inventory, review AI-generated risk assessments, and act on redistribution recommendations for their assigned facilities.

---

## 2. Getting Started

### 2.1 Logging in

1. Navigate to the application URL provided by your administrator
2. Enter your email and password
3. You will see only the facilities you are authorized to access

### 2.2 Dashboard overview

The **Executive Dashboard** shows:

- Current inventory summary (total medicines, stock levels)
- Medicines with the highest estimated stockout risk
- Batches approaching expiry within the next 90 days
- Data quality summary for your facility
- Pending redistribution recommendations awaiting review

---

## 3. Inventory Management

### 3.1 Viewing inventory

Navigate to **Inventory** to see:

- Medicine list with current stock quantities
- Inventory snapshots over time
- Recent transactions (receipts, issues, adjustments)

### 3.2 Batch and expiry tracking

Navigate to **Inventory → Batches** to see:

- All active batches with expiry dates
- Remaining shelf life for each batch
- FEFO (First Expiry, First Out) ordering

---

## 4. Understanding AI Risk Assessments

### 4.1 Stockout risk

Navigate to **Stockout Intelligence** to see:

- Risk level (Low, Medium, High, Critical) for each medicine
- Estimated days until potential stockout
- Key contributing factors (demand trend, supply delays, low stock)
- Data limitations flagged by the system

> **Important:** Risk levels are estimates, not certainties. Always consider local knowledge and context.

### 4.2 Expiry risk

Navigate to **Expiry Prevention** to see:

- Batches ranked by expiry urgency
- Projected unused quantity at expiry
- Whether the warning is date-based or model-based

### 4.3 Interpreting explanations

Each prediction includes an **Explanation** section showing:

- Which factors most influenced the prediction
- Confidence or uncertainty range
- Model version and data timestamp

These explanations describe correlations, not guaranteed causes.

---

## 5. Demand Forecasts

Navigate to **Forecasting** to view:

- Projected consumption for the next 1–6 months
- Historical consumption trend
- Uncertainty bands (where available)
- Comparison between forecast models

---

## 6. Redistribution Recommendations

### 6.1 Reviewing recommendations

Navigate to **Redistribution → Recommendations** to see suggested stock transfers:

- Source facility (donor) and destination facility (recipient)
- Medicine, quantity, and batch details
- Reason for recommendation (shortage at recipient, surplus at donor)
- Constraints satisfied (minimum stock, expiry validity, transport feasibility)

### 6.2 Approving or rejecting

- Click **Approve** to record agreement with the recommendation
- Click **Reject** with a reason to decline
- All decisions are recorded in the audit trail

> **Note:** Approving a recommendation in the system does not physically move stock. Coordinate with logistics and the other facility to execute any approved transfer.

---

## 7. Data Quality Alerts

Navigate to **Data Quality** to review:

- Missing records that may affect predictions
- Inconsistencies between recorded stock and calculated balances
- Anomalous transactions flagged for review

Address data quality issues promptly, as they directly affect the reliability of AI predictions.

---

## 8. Reports

Navigate to **Reports** to generate and export:

- Inventory status reports
- Stockout risk summaries
- Expiry risk summaries
- Forecast accuracy reports

Reports clearly distinguish observed data from predictions and recommendations.

