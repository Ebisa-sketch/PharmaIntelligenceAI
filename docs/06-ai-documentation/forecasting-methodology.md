# Medicine Demand Forecasting Methodology

---

## 1. The Forecasting Problem in Healthcare Logistics

Accurate pharmaceutical demand forecasting is complicated by several distinct structural challenges:
1. **Demand Categorization Diversity:** Within a single health center, some medicines exhibit high-volume, smooth consumption (e.g., Amoxicillin), while critical life-saving items (e.g., Antivenom, Oxytocin) show intermittent or lumpy demand with extended zero periods.
2. **Stockout Censoring:** When a clinic runs out of stock, recorded issues drop to zero. Uncorrected, algorithms interpret this as zero demand, leading to dangerous supply reductions.
3. **Small Sample Sizes:** Many facilities have only 24–36 monthly data points, making large deep neural networks prone to overfitting.

---

## 2. Demand Classification: Syntetos-Boylan Framework

Before training models, every time-series $(f, m)$ (facility $f$, medicine $m$) is classified according to the Syntetos-Boylan rules:
- **Average Inter-Demand Interval ($ADI$):** Average number of time periods between non-zero demand occurrences:
  $$ADI = \frac{N}{\sum_{t=1}^N \mathbb{I}(y_t > 0)}$$
- **Squared Coefficient of Variation ($CV^2$):** Variance of non-zero demand size divided by the square of its mean:
  $$CV^2 = \left(\frac{s_z}{\bar{z}}\right)^2$$

```
               CV^2 = 0.49
                   │
    Intermittent   │     Lumpy
       Demand      │     Demand
                   │
───────────────────┼─────────────────── ADI = 1.32
                   │
       Smooth      │     Erratic
       Demand      │     Demand
                   │
```

- **Smooth ($ADI < 1.32, CV^2 < 0.49$):** Suitable for LightGBM, Moving Averages, ARIMA.
- **Intermittent ($ADI \ge 1.32, CV^2 < 0.49$):** Croston, Syntetos-Boylan Approximation (SBA).
- **Erratic ($ADI < 1.32, CV^2 \ge 0.49$):** LightGBM with robust quantile loss.
- **Lumpy ($ADI \ge 1.32, CV^2 \ge 0.49$):** Teunter-Syntetos-Babai (TSB) or specialized hurdle models.

---

## 3. Stockout De-censoring Transformer

To correct for stockout-induced demand suppression, historical consumption is adjusted using the in-stock operating day ratio:
$$y_{t,\text{adj}} = y_{t,\text{obs}} \times \left( \frac{\text{Total Operational Days in Month } t}{\text{Days In-Stock in Month } t} \right)$$
When a facility is out of stock for $>90\%$ of the period, the observation is treated as missing and imputed using rolling median interpolation over the preceding in-stock periods.

---

## 4. Model Architectures and Formulations

### 4.1 Statistical and Intermittent Baselines
1. **Naive Baseline:** $\hat{y}_{t+h} = y_t$
2. **Seasonal Naive:** $\hat{y}_{t+h} = y_{t+h-12}$
3. **Moving Average (SMA-3 / SMA-6):** $\hat{y}_{t+h} = \frac{1}{k} \sum_{i=0}^{k-1} y_{t-i}$
4. **Croston’s Method:** Decomposes series into non-zero demand size $z_t$ and inter-arrival time $p_t$:
   $$\hat{z}_t = \hat{z}_{t-1} + \alpha (z_t - \hat{z}_{t-1})$$
   $$\hat{p}_t = \hat{p}_{t-1} + \alpha (p_t - \hat{p}_{t-1})$$
   $$\hat{y} = \frac{\hat{z}_t}{\hat{p}_t}$$
5. **Syntetos-Boylan Approximation (SBA):**
   $$\hat{y}_{\text{SBA}} = \left( 1 - \frac{\alpha}{2} \right) \frac{\hat{z}_t}{\hat{p}_t}$$
6. **Teunter-Syntetos-Babai (TSB):** Updates demand probability $d_t$ in every period:
   $$d_t = d_{t-1} + \beta (\mathbb{I}(y_t > 0) - d_{t-1})$$
   $$\hat{y}_{\text{TSB}} = d_t \cdot \hat{z}_t$$

### 4.2 Machine Learning Architecture: LightGBM Regressor
For smooth, seasonal, and erratic series, LightGBM is trained on engineered lag features:
- **Lag Features:** $y_{t-1}, y_{t-2}, y_{t-3}, y_{t-6}, y_{t-12}$.
- **Rolling Window Statistics:** 3-month and 6-month rolling mean, standard deviation, min, max.
- **Calendar & Seasonal Features:** Month of year, quarter, seasonal malaria / respiratory index.
- **Facility & Medicine Embeddings:** Categorical target encoding for facility tier and medicine therapeutic group.
- **Objective Function:** Huber Loss or Quantile Loss ($\alpha \in [0.10, 0.50, 0.90]$) to generate native prediction intervals.

---

## 5. Evaluation Metrics

Model accuracy is evaluated using scale-independent metrics suitable for zero-inflated healthcare demand:
- **Mean Absolute Scaled Error (MASE):**
  $$\text{MASE} = \frac{\frac{1}{H}\sum_{t=1}^H |y_t - \hat{y}_t|}{\frac{1}{N-1}\sum_{i=2}^N |y_i - y_{i-1}|}$$
  A value $< 1.0$ indicates superior performance compared to the in-sample naive baseline.
- **Weighted Absolute Percentage Error (WAPE):**
  $$\text{WAPE} = \frac{\sum_{t=1}^H |y_t - \hat{y}_t|}{\sum_{t=1}^H y_t}$$
- **Prediction Interval Coverage Probability (PICP):**
  Verifies that 90% prediction intervals contain the true value at least 90% of the time.
