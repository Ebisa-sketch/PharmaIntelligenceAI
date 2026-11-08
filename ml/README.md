# PharmaIntelligence AI - Machine Learning Framework

This directory houses the end-to-end Machine Learning pipelines and research components for pharmaceutical supply chain intelligence.

## Architecture Overview

```
ml/
├── common/             # Shared utilities (config, structured logging, metrics, seeds)
├── data_quality/       # Data ingestion, schema validation, anomaly detection & reconciliation
├── forecasting/        # Hierarchical demand forecasting (statistical, ML, and deep learning)
├── stockout/           # Early-warning stockout classification and risk scoring
├── expiry/             # FEFO (First-Expired, First-Out) simulation and wastage risk forecasting
├── explainability/     # Model interpretability (SHAP, feature importances, uncertainty bounds)
├── evaluation/         # Backtesting harness, model benchmarking, and performance reporting
├── pipelines/          # Modular pipelines (data, training, inference)
└── notebooks/          # Exploratory analysis and model development notebooks
```

## Analytical Modules

### 1. Common (`ml/common/`)
- **`config.py`**: Centralized configuration dataclass for hyperparameters, paths, and thresholds.
- **`logging.py`**: Standardized stream and file logging with uniform timestamps and contextual levels.
- **`metrics.py`**: Performance evaluation metrics including MAE, RMSE, MAPE, WAPE, Precision, Recall, and F1.
- **`reproducibility.py`**: Deterministic execution utilities fixing seeds across Python, NumPy, and PyTorch.

### 2. Data Quality & Reconciliation (`ml/data_quality/`)
- Preprocessing pipelines for cleaning ERP, warehouse, and transactional datasets.
- Schema verification and out-of-bounds anomaly detection.
- Inventory reconciliation across lot receipts, transfers, and inventory adjustments.

### 3. Demand Forecasting (`ml/forecasting/`)
- Multi-horizon forecasting comparing statistical baselines (ARIMA, Exponential Smoothing), gradient boosted trees (LightGBM, XGBoost, CatBoost), and sequence models (LSTM, Temporal Fusion Transformers).
- Hierarchical reconciliation across SKU, therapeutic class, facility, and regional levels.

### 4. Stockout Risk Classification (`ml/stockout/`)
- Binary classification predicting probability of stock exhaustion within operational lead times.
- Feature engineering combining inventory run-out velocity, supplier lead-time variability, and demand surges.

### 5. Expiry & FEFO Management (`ml/expiry/`)
- Lot-level remaining shelf life (RSL) tracking.
- Simulation of First-Expired, First-Out (FEFO) dispensing policies vs FIFO.
- Wastage hazard forecasting to identify at-risk batches before critical expiry windows.

### 6. Explainability & Trust (`ml/explainability/`)
- SHAP (SHapley Additive exPlanations) values for global and local feature importance.
- Uncertainty estimation through conformal prediction and prediction intervals.

### 7. Evaluation & Backtesting (`ml/evaluation/`)
- Rolling-window time-series backtesting preserving temporal order.
- Automated champion-challenger model comparison and markdown/PDF report generation.

### 8. Pipelines (`ml/pipelines/`)
- **`data_pipeline.py`**: Ingestion and validation orchestrator.
- **`training_pipeline.py`**: Model training, tuning, and artifact serialization.
- **`inference_pipeline.py`**: Batch scoring and real-time inference serving.
