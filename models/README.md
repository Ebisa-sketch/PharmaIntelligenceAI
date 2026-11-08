# PharmaIntelligence AI - Machine Learning Models & Artifacts

This directory stores trained ML model artifacts, training configurations, serialization schemas, and model registry records for the PharmaIntelligence AI analytics engine.

## Structure

- **`artifacts/`**: Serialized binary models (LightGBM, XGBoost, Prophet, PyTorch, Scikit-Learn pipelines) and feature preprocessors.
  - `data_quality/`: Anomaly detectors, outlier isolation forests, imputation weights.
  - `forecasting/`: Demand forecasting checkpoints (TFT, DeepAR, LightGBM multi-horizon regressors).
  - `stockout/`: Early-warning classification models predicting probability of stock depletion.
  - `expiry/`: Batch survival and risk-of-wastage models.
- **`configurations/`**: YAML/JSON hyperparameter configuration sets and training pipeline specifications.
- **`model_registry/`**: Model versioning metadata, MLflow tracking runs, and performance evaluation cards.

## Model Lifecycle & Deployment

1. **Training**: Orchestrated via `scripts/ml/train_models.py`.
2. **Evaluation**: Regression (RMSE, MASE, WAPE) and classification metrics (PR-AUC, F1-macro) generated via `scripts/ml/evaluate_models.py`.
3. **Serving**: Loaded asynchronously by the FastAPI inference service.
