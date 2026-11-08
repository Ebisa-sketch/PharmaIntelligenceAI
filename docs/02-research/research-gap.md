# Research Gap Analysis

---

## 1. Overview

While extensive academic research exists in supply chain forecasting, perishable inventory theory, and healthcare informatics independently, significant methodological and practical gaps persist at their intersection—particularly within resource-constrained public healthcare settings like Ethiopia.

This document formalizes the specific research and engineering gaps that PharmaIntelligence AI targets.

---

## 2. Identified Research Gaps

### Gap 1: Disconnection Between Inventory Data Quality and Predictive Analytics
- **Current State:** Most machine learning forecasting and inventory models assume pristine, standardized input data. In academic benchmarks (e.g., M5 forecasting competition), data are pre-cleaned with complete transaction logs.
- **The Reality in LMICs:** Health facility data suffer from frequent missing entries, manual transcription errors, broken reconciliation balances (`Opening + In - Out != Closing`), and irregular reporting intervals.
- **The Gap:** There is an acute lack of end-to-end frameworks that quantitatively profile, score, and sanitize noisy health facility inventory logs *prior* to feeding them into predictive models, while transparently warning users when data quality falls below reliable thresholds.

### Gap 2: Neglect of Stockout Censoring in Healthcare Demand Forecasting
- **Current State:** Existing public health forecasting in LMICs relies heavily on historical Monthly Average Consumption (MAC). When machine learning models are evaluated in research, they frequently train on unadjusted consumption series.
- **The Reality in LMICs:** When a facility experiences an essential medicine stockout (e.g., 25 days out of stock in a month), recorded issues are artificially suppressed near zero. True clinical demand remains high, but patient requests go unfulfilled.
- **The Gap:** Traditional models treat stockout periods as genuine drops in demand, leading to downward forecast spirals (lower consumption $\rightarrow$ lower forecast $\rightarrow$ reduced replenishment $\rightarrow$ chronic stockout). Practical, computationally lightweight demand de-censoring algorithms tailored for facility-level eLMIS datasets are rarely integrated into operational tools.

### Gap 3: Reactive Expiry Disposal vs. Predictive Batch Waste Estimation
- **Current State:** Conventional inventory management monitors batch expiry dates using passive thresholds (e.g., "alert when batch is within 90 days of expiry").
- **The Reality in LMICs:** A batch expiring in 90 days with 10 units in stock at a hospital dispensing 50 units per month is at **zero risk** of expiry. Conversely, a batch expiring in 180 days with 5,000 units at a rural health center dispensing 50 units per month is at **guaranteed risk** of substantial waste.
- **The Gap:** Current systems fail to dynamically intersect batch-level FEFO queue dynamics with forward-looking stochastic demand forecasts to calculate the exact *Projected Unused Quantity at Expiry*.

### Gap 4: Centralized Vertical Distribution vs. Algorithmic Lateral Redistribution
- **Current State:** Public healthcare supply chains are predominantly organized vertically (central warehouse $\rightarrow$ regional hub $\rightarrow$ health facility). Stock redistribution across facilities is handled through informal phone calls, emergency manual requisitions, or ad-hoc administrative directives.
- **The Reality in LMICs:** Significant geographic stock imbalances exist simultaneously: one clinic faces an acute stockout of oral rehydration salts or insulin while a sister clinic 30 kilometers away holds expiring surplus.
- **The Gap:** There is an absence of formal, constrained optimization models (e.g., Mixed-Integer Linear Programming) designed specifically for lateral peer-to-peer transfers among public health facilities that explicitly respect transport feasibility, shelf-life viability, and donor safety-stock protection.

### Gap 5: The "Black Box" Barrier in Clinical Decision Support
- **Current State:** Modern machine learning models (gradient boosted trees, neural networks) deliver superior empirical accuracy but behave as opaque black boxes.
- **The Reality in LMICs:** Healthcare professionals and supply chain managers are legally and ethically accountable for medicine availability. They will not execute redistributions or modify ordering behavior based on uninterpretable algorithmic confidence scores.
- **The Gap:** Few pharmaceutical inventory platforms integrate explainable AI techniques (e.g., SHAP, counterfactual diagnostics, and prediction intervals) into a practical, role-tailored user experience that builds user trust and facilitates human review.

---

## 3. Summary Gap-to-Solution Mapping

```
┌────────────────────────────────────────────────────────┐
│                      RESEARCH GAPS                     │
├──────────────────────────┬─────────────────────────────┤
│ 1. Data Quality Gap      │ 2. Stockout Censoring Gap   │
│ 3. Reactive Expiry Gap   │ 4. Lateral Transshipment Gap│
│ 5. Opaque AI Black Box   │                             │
└──────────────────────────┴─────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│              PHARMAINTELLIGENCE AI MODULES             │
├──────────────────────────┬─────────────────────────────┤
│ 1. Data Quality Intel    │ 2. De-censored Forecasting  │
│ 3. FEFO Expiry Engine    │ 4. MILP Redistribution      │
│ 5. TreeSHAP + XAI UI     │                             │
└────────────────────────────────────────────────────────┘
```

By systematically addressing these five interconnected gaps, PharmaIntelligence AI establishes an innovative, scientifically sound, and socially impactful contribution to healthcare informatics.
