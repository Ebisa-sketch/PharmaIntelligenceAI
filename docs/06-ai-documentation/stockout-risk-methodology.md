# Stockout Risk Intelligence Methodology

---

## 1. Problem Formulation

Stockout risk modeling addresses the fundamental operational question:
> *"What is the probability that usable inventory of medicine $m$ at facility $f$ will drop to zero within planning horizon $H$ (e.g., 30 or 60 days) before replenishment arrives?"*

Rather than relying purely on deterministic Days-of-Stock thresholds, PharmaIntelligence AI develops a **calibrated probabilistic classification framework** that integrates demand volatility and supplier lead-time uncertainty.

---

## 2. Risk Estimation Formulations

### 2.1 Deterministic Inventory Rule: Days of Stock Remaining (DSR)
The baseline operational metric is Days of Stock Remaining:
$$\text{DSR}_{f,m} = \frac{I_{f,m}}{\hat{d}_{f,m}}$$
where $I_{f,m}$ is current usable stock on hand, and $\hat{d}_{f,m}$ is the projected daily demand from the forecasting engine.
- If $\text{DSR} < L_{\text{expected}}$ (expected supplier lead time), the item is in high stockout danger.

### 2.2 Supervised Machine Learning Formulation
To account for lead-time variability and pending pipeline orders, stockout risk is formulated as a binary classification problem:
$$Y_{f,m,t}^{(H)} \in \{0, 1\}$$
where $Y=1$ indicates that inventory hit zero at any point between $t$ and $t+H$.

#### Feature Vector $\mathbf{x}_{f,m,t}$:
1. **Inventory Ratios:**
   - $\text{DSR} / L_{\text{expected}}$: Stock coverage relative to expected lead time.
   - Safety Stock Buffer Ratio: $(I - SS) / SS$.
2. **Pipeline Order Features:**
   - Indicator of open pending purchase order ($\mathbb{I}_{\text{order}}$).
   - Elapsed days since order placement vs. historical median lead time.
   - Open order quantity relative to monthly demand.
3. **Demand Volatility Features:**
   - 90th percentile demand forecast ($P_{90}$) divided by mean forecast.
   - Demand Coefficient of Variation ($CV$).
4. **Historical Supply Reliability:**
   - Historical stockout frequency for this medicine over the past 12 months.
   - EPSS regional hub historical lead-time standard deviation.

---

## 3. Candidate Classifiers and Calibration

The framework trains and benchmarks three candidate classifiers:
1. **Logistic Regression (Baseline):** Transparent linear log-odds model providing immediate coefficient interpretability.
2. **Random Forest Classifier:** Robust against feature collinearity and outliers.
3. **LightGBM / XGBoost Classifier:** Gradient-boosted decision trees optimizing binary cross-entropy with scale-pos-weight adjustment for class imbalance.

### Probability Calibration
Raw tree probabilities can be uncalibrated. The model applies **Isotonic Regression** on an out-of-fold calibration set to ensure that:
$$\mathbb{P}(\text{Stockout} \mid \hat{p} = 0.80) \approx 0.80$$
Calibration quality is evaluated using the **Brier Score**:
$$\text{Brier} = \frac{1}{N}\sum_{i=1}^N (\hat{p}_i - y_i)^2$$

---

## 4. Operational Risk Stratification

Predictions are mapped into intuitive operational tiers for pharmacy managers:

| Risk Tier | Calibrated Probability | Days of Stock Remaining (DSR) | Recommended Action |
|---|---|---|---|
| **CRITICAL** | $p \ge 0.75$ | $\text{DSR} < 14\text{ days}$ | Immediate lateral transfer request / Emergency requisition |
| **HIGH** | $0.50 \le p < 0.75$ | $14 \le \text{DSR} < 30\text{ days}$ | Alert regional coordinator; prioritize incoming EPSS dispatch |
| **MODERATE** | $0.25 \le p < 0.50$ | $30 \le \text{DSR} < 60\text{ days}$ | Routine monitoring; schedule regular replenishment order |
| **SAFE** | $p < 0.25$ | $\text{DSR} \ge 60\text{ days}$ | Normal inventory status; evaluate possible excess |
