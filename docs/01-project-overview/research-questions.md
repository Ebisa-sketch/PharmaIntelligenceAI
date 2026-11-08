# Research Questions and Hypotheses

PharmaIntelligence AI investigates the synthesis of data quality profiling, machine learning forecasting, risk classification, explainability, and mathematical optimization within healthcare supply chains. The project is organized around six foundational Research Questions (RQs).

---

## Research Question 1: Inventory Data Quality Assessment
> **RQ1:** How can incomplete, inconsistent, and stockout-censored pharmaceutical inventory data in resource-constrained health facilities be systematically detected, validated, and quantified before analytical modeling?

- **Hypothesis (H1):** Rule-based reconciliation algorithms combined with statistical anomaly detection (IQR and Isolation Forests) can identify >95% of artificial or documented inventory discrepancies (e.g., negative stock, broken reconciliation equations, impossible transaction rates) without corrupting underlying transaction provenance.
- **Key Metrics:** Precision, Recall, F1-Score of anomaly identification; Percentage of reconciled inventory balances; Data Quality Completeness Index (DQCI).
- **Analytical Method:** Compare standard raw ingestion against a two-stage Data Quality Intelligence (DQI) pipeline performing Pydantic structural validation followed by transaction ledger balance verification (`Opening + Receipts - Issues + Adjustments = Closing`).

---

## Research Question 2: Demand Forecasting Under Intermittency and Censoring
> **RQ2:** Which forecasting methods provide superior accuracy, stability, and computational efficiency for essential medicines exhibiting intermittent demand and historical stockout censoring?

- **Hypothesis (H2):** Machine learning models (e.g., LightGBM / XGBoost) trained on de-censored demand features will achieve a statistically significant reduction in forecast error (lower MASE and WAPE) compared to traditional time-series baselines (Moving Average, Croston, Seasonal Naive) across irregular consumption patterns.
- **Key Metrics:** Mean Absolute Scaled Error (MASE), Weighted Absolute Percentage Error (WAPE), Root Mean Squared Error (RMSE), Prediction Interval Coverage Probability (PICP).
- **Analytical Method:** Time-series cross-validation using rolling-origin backtesting over a 24- to 36-month timeline, evaluating performance across smooth, intermittent, erratic, and lumpy demand categories (Syntetos-Boylan Classification).

---

## Research Question 3: Probabilistic Stockout Risk Modeling
> **RQ3:** How accurately can the risk and expected lead time to stock exhaustion be predicted by combining inventory levels, demand forecasts, and lead-time distributions?

- **Hypothesis (H3):** A supervised classification model incorporating dynamic demand uncertainty and supplier lead-time distributions will predict stockouts occurring within 30 to 60 days with a higher PR-AUC and lower false-alarm rate than static Days of Stock Remaining (DSR) threshold heuristics.
- **Key Metrics:** Precision, Recall, Area Under the Precision-Recall Curve (PR-AUC), Brier Score (calibration error), False Discovery Rate (FDR).
- **Analytical Method:** Train and evaluate Logistic Regression, Random Forest, and Gradient Boosted trees on engineered features (current usable stock, replenishment order status, historical delivery delay variance, forecast quantiles) against confirmed historical stockout intervals.

---

## Research Question 4: Batch-Level Expiry Prevention
> **RQ4:** How can batch-level expiration risks be modeled using First-Expired-First-Out (FEFO) consumption simulations paired with probabilistic demand forecasts?

- **Hypothesis (H4):** Combining forward-looking demand distributions with FEFO depletion queues can identify at least 80% of expired batch volume at least 90 days before expiration, providing actionable lead time for operational intervention.
- **Key Metrics:** Lead time of expiry identification (days prior to expiry); False Alarm Rate for expiry warnings; Volume and monetary value of accurately predicted expired units.
- **Analytical Method:** Deterministic FEFO queue simulation evaluated against actual batch consumption trajectories, testing sensitivity across varying demand volatility levels.

---

## Research Question 5: Constrained Lateral Stock Redistribution
> **RQ5:** Under what logistical, clinical, and financial constraints can mixed-integer linear programming (MILP) inter-facility stock redistribution minimize net system stockouts and batch expiries?

- **Hypothesis (H5):** Multi-facility MILP redistribution optimization will reduce total simulated system stockout days by >25% and expired units by >30% compared to isolated facility operations, while ensuring donor safety stock is preserved.
- **Key Metrics:** Reduction in stockout hours/days; Reduction in expired inventory value (ETB / USD); Total transfer distance/cost; Number of transfer transactions generated; Donor post-transfer stockout incidence.
- **Analytical Method:** Discrete-event simulation comparing baseline disconnected facilities against an OR-Tools / Pyomo optimization model with constraints on donor safety stock, remaining shelf life, transport distance, and storage compatibility.

---

## Research Question 6: Explainability and Decision-Support Usability
> **RQ6:** How does the integration of feature-attribution explanations (e.g., TreeSHAP) and uncertainty intervals impact user trust, decision latency, and recommendation adoption among pharmacy personnel?

- **Hypothesis (H6):** Providing localized factor contribution breakdowns and prediction intervals will significantly increase pharmacist agreement with correct model recommendations and increase the detection of erroneous recommendations compared to black-box outputs.
- **Key Metrics:** User agreement rate with validated transfer recommendations; Pharmacist subjective trust score (SUS scale); Time taken to evaluate and decide upon a proposed recommendation.
- **Analytical Method:** Structured user evaluation and scenario-based simulated walkthroughs contrasting black-box score outputs with transparent SHAP explanations and uncertainty bounds.
