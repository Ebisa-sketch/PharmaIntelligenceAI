# Data Analyst / Researcher Guide

## PharmaIntelligence AI — Researcher Manual

> **Document status:** Draft  
> **Last updated:** 2026-11-05

---

## 1. Overview

This guide is for **Data Analysts and Researchers** who use PharmaIntelligence AI to import datasets, assess data quality, configure and run AI experiments, and evaluate model performance.

---

## 2. Data Import Workflow

### 2.1 Preparing data

Before importing, ensure your CSV file:

- Uses the expected column names (see `docs/05-data-documentation/data-dictionary.md`)
- Contains valid date formats (YYYY-MM-DD)
- Uses consistent medicine identifiers and units
- Does not contain patient-identifiable information

### 2.2 Importing data

1. Navigate to **Inventory → Import** (or use the API endpoint `POST /api/v1/imports`)
2. Select the data type (consumption, inventory snapshot, batch, transaction)
3. Upload the CSV file
4. Review the validation report — rows with errors are flagged but not silently discarded
5. Confirm the import

### 2.3 Import provenance

Every import records:

- Source file name and hash
- Upload timestamp and uploading user
- Row counts (total, accepted, rejected)
- Validation errors

---

## 3. Data Quality Assessment

### 3.1 Running quality checks

Navigate to **Data Quality Center** to:

- View automatic quality assessments on imported data
- Inspect missing values, duplicates, and type mismatches
- Review stock reconciliation differences
- Examine anomaly flags (IQR-based or Isolation Forest)

### 3.2 Quality metrics

| Metric | Description |
|--------|-------------|
| Completeness | Percentage of non-null values per field |
| Consistency | Reconciliation between opening stock, transactions, and closing stock |
| Uniqueness | Duplicate record detection rate |
| Anomaly rate | Proportion of statistically unusual values |

---

## 4. Running Experiments

### 4.1 AI Model Laboratory

Navigate to **AI Laboratory** to:

- Select a dataset version
- Choose a model type (forecasting, stockout risk, expiry risk)
- Configure model parameters and features
- Run training with automatic chronological train/validation/test splits

### 4.2 Experiment tracking

Each experiment records:

- Dataset version and preprocessing steps
- Model type, hyperparameters, and random seed
- Training and evaluation periods
- Performance metrics (MAE, RMSE, WAPE, MASE for forecasting; Precision, Recall, F1, PR-AUC for classification)
- Feature importance and SHAP explanations

### 4.3 Baseline comparisons

Every experiment should be compared against baselines:

| Task | Baseline |
|------|----------|
| Forecasting | Naive forecast, seasonal naive, moving average |
| Stockout risk | Inventory threshold rules |
| Expiry risk | Deterministic FEFO calculation |

---

## 5. Forecasting Experiments

### 5.1 Available models

- **Statistical:** ARIMA, SARIMA, Croston/TSB (intermittent demand)
- **Machine learning:** Random Forest, XGBoost
- **Deep learning:** LSTM (optional, requires sufficient data volume)

### 5.2 Key considerations

- **Stockout censoring:** Low recorded issues during stockouts may understate true demand. Investigate and document this effect.
- **Chronological splits:** Never use random train/test splits for time-series data
- **Rolling-origin backtesting:** Use expanding or sliding window evaluation for robust metrics

---

## 6. Model Evaluation

### 6.1 Metrics

Navigate to **AI Laboratory → Evaluation** to compare models:

- Forecasting: MAE, RMSE, WAPE, MASE, prediction interval coverage
- Classification: Precision, Recall, F1, PR-AUC, calibration curves
- Optimization: Constraint satisfaction rate, simulated stockout reduction, simulated expiry reduction

### 6.2 Model comparison

View side-by-side metric tables and plots to determine which model performs best under different data conditions (e.g., high vs. low volume medicines, intermittent demand patterns).

---

## 7. Explainability Tools

### 7.1 SHAP explanations

For tree-based models, SHAP values show which features most influenced each prediction. Access SHAP plots from the experiment detail page.

### 7.2 Feature importance

Global feature importance rankings help understand which data fields drive model behaviour across the dataset.

### 7.3 Uncertainty quantification

Where supported, review prediction intervals and confidence levels. Wider intervals indicate greater uncertainty.

---

## 8. Reproducibility

### 8.1 Reproducing an experiment

Every experiment page includes:

- Exact dataset version used
- Full configuration (hyperparameters, features, random seed)
- Preprocessing pipeline steps
- Code version (Git commit hash)

### 8.2 Best practices

- Always document data exclusions and preprocessing decisions
- Record negative results — they are scientifically valuable
- Distinguish results from real data vs. synthetic data
- Do not claim real-world effectiveness from synthetic experiments

---

## 9. API Access

Researchers can also interact with the system programmatically:

| Endpoint | Purpose |
|----------|---------|
| `POST /api/v1/imports` | Upload datasets |
| `GET /api/v1/data-quality/{dataset_id}` | Retrieve quality reports |
| `POST /api/v1/experiments` | Create and run experiments |
| `GET /api/v1/experiments/{id}/results` | Retrieve experiment results |
| `GET /api/v1/forecasting/{medicine_id}` | Get forecast outputs |

Refer to `docs/04-system-design/api-design.md` for the full API specification.

