# Machine Learning Model Evaluation Plan and Experimental Benchmarking

---

## 1. Evaluation Philosophy and Rigor

To prevent common empirical pitfalls in supply chain machine learning (such as look-ahead bias, data leakage, and uncalibrated probabilities), PharmaIntelligence AI enforces a strict evaluation protocol:
1. **Strict Chronological Splitting:** Under no circumstances are time-series records randomly shuffled. All train/test partitions follow chronological order.
2. **Transparent Baseline Comparators:** Every complex machine learning algorithm must be evaluated against established transparent baselines (e.g., Seasonal Naive, Moving Average, Croston).
3. **Multi-Faceted Evaluation Metrics:** Models are scored on point accuracy, tail coverage, calibration error, and computational latency.

---

## 2. Cross-Validation: Rolling-Origin Backtesting

The evaluation harness implements **Rolling-Origin Cross-Validation** (walk-forward backtesting) over a 36-month timeline:

```
Split 1: [--- Train: Months 1–24 ---][ Val: 25–27 ][ Test: 28–30 ]
Split 2: [--- Train: Months 1–27 ---][ Val: 28–30 ][ Test: 31–33 ]
Split 3: [--- Train: Months 1–30 ---][ Val: 31–33 ][ Test: 34–36 ]
```

- **Origin Update:** The forecasting origin rolls forward by $H=3$ months in each split.
- **Model Refitting:** Feature matrices and model weights are recomputed at each step using only historical information available prior to the origin.

---

## 3. Comprehensive Metric Definitions

### 3.1 Demand Forecasting Metrics

| Metric | Formula | Target Threshold | Interpretation |
|---|---|---|---|
| **MASE** | $\frac{\frac{1}{H}\sum |y_t - \hat{y}_t|}{\frac{1}{N-1}\sum |y_i - y_{i-1}|}$ | $< 0.85$ | Scale-free; $< 1.0$ beats in-sample naive baseline |
| **WAPE** | $\frac{\sum |y_t - \hat{y}_t|}{\sum y_t}$ | $< 25\%$ | Volume-weighted error percentage |
| **RMSE** | $\sqrt{\frac{1}{H}\sum (y_t - \hat{y}_t)^2}$ | Minimize | Penalizes large forecasting errors heavily |
| **PICP (90%)** | $\frac{1}{H}\sum \mathbb{I}(y_t \in [\hat{L}_t, \hat{U}_t])$ | $\ge 88\%$ | Prediction Interval Coverage Probability |

### 3.2 Stockout Risk Classification Metrics

| Metric | Formula / Description | Target Threshold | Interpretation |
|---|---|---|---|
| **PR-AUC** | Area under Precision-Recall curve | $> 0.75$ | Critical for imbalanced binary stockout labels |
| **F1-Score** | $2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$ | $> 0.80$ | Harmonic mean of precision and recall |
| **Brier Score** | $\frac{1}{N}\sum (\hat{p}_i - y_i)^2$ | $< 0.12$ | Measures probabilistic prediction calibration |
| **False Discovery Rate** | $\frac{\text{FP}}{\text{TP} + \text{FP}}$ | $< 15\%$ | Minimizes "alarm fatigue" for pharmacy staff |

---

## 4. End-to-End System Simulation Evaluation

Beyond standalone algorithm metrics, the entire system is evaluated via a **Discrete-Event Simulation (SimPy)** modeling a network of 5 public healthcare facilities over 12 operational months.

### Simulated Policy Comparisons:
1. **Policy 0 (Status Quo Baseline):** Facilities order inventory using static historical Monthly Average Consumption (MAC) without lateral transfers.
2. **Policy 1 (Forecast-Driven):** Facilities order based on LightGBM demand forecasts, but remain isolated (no lateral transfers).
3. **Policy 2 (Reactive Lateral Transfers):** Emergency transfers requested only after stockout occurs.
4. **Policy 3 (PharmaIntelligence AI Integrated):** De-censored LightGBM forecasts + Probabilistic Stockout/Expiry Risk + Proactive MILP Redistribution.

### System-Level Outcome Indicators:
- **Total Stockout Days:** Sum of medicine stockout days across all 5 facilities.
- **Total Expired Quantity:** Total physical units reaching expiry.
- **Expired Value at Risk (ETB):** Monetary value of discarded inventory.
- **System Service Level:** Percentage of total patient demand successfully dispensed on time.
- **Net Logistical Cost:** Total cost of transportation and ordering across the network.
