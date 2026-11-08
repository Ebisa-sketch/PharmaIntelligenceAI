# Research and Experimental Methodology

---

## 1. Methodological Framework Overview

PharmaIntelligence AI employs an applied, multi-disciplinary research methodology combining **Design Science Research (DSR)**, quantitative statistical evaluation, and discrete-event simulation. The methodology is structured to ensure rigorous empirical validation while addressing practical constraints encountered in low-resource healthcare logistics.

```
┌────────────────────────────────────────────────────────────────────────┐
│                   DSR ITERATIVE RESEARCH CYCLE                         │
├───────────────┬────────────────┬───────────────┬───────────────────────┤
│ 1. Problem    │ 2. Artifact    │ 3. Algorithmic│ 4. Empirical          │
│ Identification│    Design      │    Execution  │    Evaluation         │
│ & Data Audit  │ & Mathematical │ & Comparative │ & Simulation          │
│               │   Formulation  │    Modeling   │    Validation         │
└───────────────┴────────────────┴───────────────┴───────────────────────┘
```

---

## 2. Experimental Stages

### Stage 1: Data Acquisition, Profiling, and Synthesis
1. **Secondary Data Review:** Systematic audit of accessible published Ethiopian pharmaceutical datasets, noting observation periods, frequency, medicine categories, and data limitations.
2. **Realistic Synthetic Benchmarking:** In parallel with real data access protocols, construct a parameterized synthetic dataset generator based on published Ethiopian health logistics characteristics (EPSS lead-time distributions, morbidity seasonal patterns, intermittent consumption frequencies, and random anomaly injection).
3. **Data Quality Scoring:** Establish quantitative thresholds for missingness, duplication, ledger mismatch, and invalid date sequences.

### Stage 2: Time-Series Cross-Validation and Forecasting Benchmarking
1. **Demand Categorization:** Classify medicine demand series using the Syntetos-Boylan criteria based on Average Inter-Demand Interval ($ADI$) and Squared Coefficient of Variation ($CV^2$):
   - Smooth ($ADI < 1.32, CV^2 < 0.49$)
   - Intermittent ($ADI \ge 1.32, CV^2 < 0.49$)
   - Erratic ($ADI < 1.32, CV^2 \ge 0.49$)
   - Lumpy ($ADI \ge 1.32, CV^2 \ge 0.49$)
2. **Backtesting Strategy:** Employ **rolling-origin backtesting** (chronological walk-forward validation). Avoid random row shuffling to eliminate future data leakage.
   - Example 36-month series: 24 months training, 6 months validation, 6 months out-of-sample testing.
3. **Model Portfolio:**
   - *Baselines:* Naive, Seasonal Naive, Simple Moving Average (SMA-3, SMA-6).
   - *Specialized Intermittent Models:* Croston’s method, Syntetos-Boylan Approximation (SBA), Teunter-Syntetos-Babai (TSB).
   - *Machine Learning:* LightGBM, XGBoost, and CatBoost with lag features, calendar seasonality, and rolling statistics.
   - *De-censoring Experiments:* Compare raw consumption series against in-stock adjusted series ($y_{adj} = y_{obs} \times \frac{\text{Total Days}}{\text{In-Stock Days}}$).

### Stage 3: Supervised Stockout Risk Modeling
1. **Problem Formulation:** Formulate multi-horizon stockout prediction (e.g., $t+30$, $t+60$ days) as a binary classification problem:
   $$Y_{i,t,h} \in \{0, 1\}$$
   where $Y=1$ indicates usable stock reaching zero within horizon $h$ at facility $i$.
2. **Feature Engineering:**
   - Days of Stock Remaining: $\text{DSR} = \frac{\text{Current Usable Stock}}{\hat{D}_{\text{daily}}}$
   - Ratio of pipeline orders to safety stock
   - Historical lead-time standard deviation
   - Forecast lower/upper uncertainty bounds ($P_{10}, P_{50}, P_{90}$)
3. **Model Evaluation:**
   - Due to class imbalance, prioritize **Precision-Recall AUC (PR-AUC)** and **F1-Score** over ROC-AUC.
   - Calibrate output probabilities using isotonic regression and assess via Brier score.

### Stage 4: Perishable Inventory and Expiry Risk Formulation
1. **Queue Simulation:** Model facility batch inventory as a priority queue sorted by ascending expiry date ($\text{Exp}_1 \le \text{Exp}_2 \le \dots \le \text{Exp}_k$).
2. **Cumulative Depletion Mapping:** Intersect the cumulative demand trajectory $\int_{0}^{T} \hat{D}(t) dt$ against batch quantities to calculate:
   $$\text{Projected Waste}_b = \max\left(0, Q_b - \sum_{t=0}^{\text{Exp}_b} \hat{D}(t)\right)$$
3. **Threshold vs. Model Comparison:** Compare simple date-threshold alerts against forecast-assisted projected waste volume.

### Stage 5: Constrained Redistribution Optimization and Simulation
1. **Formulation:** Mixed-Integer Linear Program (MILP) solved using Google OR-Tools.
   - *Objective:* Minimize total penalty costs:
     $$\min \sum \left( C_{\text{shortage}} \cdot \text{UnmetNeed} + C_{\text{waste}} \cdot \text{ExpiredQty} + C_{\text{transport}} \cdot d_{ij} \cdot x_{ijbm} \right)$$
   - *Constraints:* Non-negativity, batch conservation, donor minimum safety threshold, maximum travel radius, and recipient shelf-life viability.
2. **Discrete-Event Simulation (SimPy):**
   - Simulate a regional network of 5–10 health facilities over a 12-month period.
   - Compare four operational policies:
     1. Baseline: Isolated facility operations (no transfers).
     2. Static Rule: Manual emergency transfer requests upon stockout.
     3. Forecast-Only: Reordering triggered by ML demand forecasts without lateral transfers.
     4. Integrated PharmaIntelligence AI: Proactive ML forecasting + Stockout Risk + MILP Lateral Redistribution.

### Stage 6: Explainable AI and Human-in-the-Loop Validation
1. **Explainability Architecture:** Compute TreeSHAP explanations for LightGBM/XGBoost predictions to extract top-5 positive and negative contributing features.
2. **Decision Usability Review:** Conduct scenario-based structured walkthroughs with clinical/pharmacy subject matter experts to evaluate explanation clarity, trust, and actionable utility.

---

## 3. Evaluation Metrics Summary

| Research Area | Primary Metric | Secondary Metrics |
|---|---|---|
| **Data Quality** | Anomaly Detection F1-Score | Data Completeness Index, Reconciliation Error Rate |
| **Forecasting** | MASE (Mean Absolute Scaled Error) | WAPE, RMSE, Prediction Interval Coverage (PICP) |
| **Stockout Risk** | PR-AUC (Precision-Recall Area) | F1-Score, Brier Calibration Score, False Alarm Rate |
| **Expiry Risk** | Timeliness (Lead time to expiry in days) | Unused Waste Detection Recall, False Alarm Rate |
| **Redistribution** | % Reduction in System Stockout Days | % Reduction in Expired Inventory Value, Net Transfer Cost |
| **Explainability** | Pharmacist Decision Agreement Rate | System Usability Scale (SUS), Decision Latency |
