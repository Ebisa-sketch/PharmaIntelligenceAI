# PharmaIntelligence AI - Research and Experimentation Log

## Objectives
1. Formulate robust intermittent and seasonal pharmaceutical demand forecasting models.
2. Develop probabilistic early-warning systems for critical medicine stockouts with a 14-day and 30-day lookahead.
3. Optimize near-expiry batch reallocation across distributed regional nodes minimizing transport costs and discarding waste.

---

## Log Entries

### [2026-11-01] - Setup & Problem Formulation
- **Author**: Research Team
- **Focus**: Baseline demand modeling for high-velocity vs. intermittent SKUs.
- **Observations**: Croston's method and LightGBM with rolling-window statistics outperform naive ARIMA on erratic hospital consumption records.
- **Next Steps**: Benchmark Temporal Fusion Transformers (TFT) against gradient-boosted decision trees.

### [2026-11-03] - Experiment 001: Baseline Demand Regressors
- **Status**: Completed
- **Findings**: LightGBM achieved WAPE of 14.2% on continuous demand drugs. Intermittent antibiotic fills require specialized zero-inflated Poisson or Tweedie loss functions.

### [2026-11-05] - Experiment 002: Stockout Probability Classifier
- **Status**: In-Progress
- **Features Tested**: Lead-time variability, supplier fill rate, days-of-supply, historical buffer depletion rate.
- **Goal**: Target PR-AUC >= 0.88 with 90%+ recall on life-saving medicine categories.
