# RESTful API Design Specification

---

## 1. Overview and Standards

PharmaIntelligence AI exposes an **OpenAPI 3.1**-compliant RESTful interface. All request and response bodies utilize standard JSON encoding (UTF-8).

### Standard Headers:
- `Content-Type: application/json`
- `Authorization: Bearer <jwt_access_token>`
- `X-Correlation-ID: <uuid>` (for distributed request tracing)

### Standard HTTP Status Codes:
- `200 OK`: Successful synchronous operation.
- `201 Created`: Resource created successfully.
- `202 Accepted`: Asynchronous long-running job queued (e.g., optimization run).
- `400 Bad Request`: Validation failure or malformed payload.
- `401 Unauthorized`: Missing or expired authentication token.
- `403 Forbidden`: Insufficient role or facility scope permissions.
- `404 Not Found`: Resource does not exist.
- `422 Unprocessable Entity`: Semantic validation failure (Pydantic).
- `500 Internal Server Error`: Unhandled server exception.

---

## 2. API Endpoints Catalog

### 2.1 Authentication & Profile (`/api/v1/auth`)

| Method | Endpoint | Description | Roles |
|---|---|---|---|
| `POST` | `/api/v1/auth/login` | Authenticate user with credentials, return JWT | Public |
| `POST` | `/api/v1/auth/refresh` | Refresh expired access token using HTTP-only cookie | Public |
| `POST` | `/api/v1/auth/logout` | Revoke current user session | Authenticated |
| `GET` | `/api/v1/auth/me` | Fetch active user profile, roles, and facility scope | Authenticated |

---

### 2.2 Facility & Medicine Reference (`/api/v1/reference`)

| Method | Endpoint | Description | Roles |
|---|---|---|---|
| `GET` | `/api/v1/reference/facilities` | List authorized facilities with geographic coordinates | All |
| `GET` | `/api/v1/reference/facilities/{id}` | Retrieve specific facility details | All |
| `GET` | `/api/v1/reference/medicines` | Query medicine catalog with filtering & search | All |
| `POST` | `/api/v1/reference/medicines` | Register new master medicine definition | Admin |

---

### 2.3 Data Ingestion & Quality Intelligence (`/api/v1/data`)

| Method | Endpoint | Description | Roles |
|---|---|---|---|
| `POST` | `/api/v1/data/upload` | Multipart upload of CSV/Excel inventory transaction file | Admin, Manager, Officer |
| `GET` | `/api/v1/data/imports` | List previous data import runs with summary stats | Admin, Manager, Officer, Researcher |
| `GET` | `/api/v1/data/imports/{id}/issues`| Retrieve detailed data-quality error log for import | Admin, Manager, Officer, Researcher |
| `GET` | `/api/v1/data/quality-score/{facility_id}` | Get aggregate Data Quality Completeness Index (DQCI) | All |

---

### 2.4 Inventory & Batch Management (`/api/v1/inventory`)

| Method | Endpoint | Description | Roles |
|---|---|---|---|
| `GET` | `/api/v1/inventory/stock-summary` | Aggregated stock position per facility and medicine | All |
| `GET` | `/api/v1/inventory/batches` | Query active batches with shelf life and status | All |
| `GET` | `/api/v1/inventory/transactions` | Query ledger transactions with date and type filters | All |

---

### 2.5 Demand Forecasting (`/api/v1/forecasting`)

| Method | Endpoint | Description | Roles |
|---|---|---|---|
| `GET` | `/api/v1/forecasting/predict` | Generate on-the-fly forecast for medicine & facility | All |
| `GET` | `/api/v1/forecasting/compare-models` | Return comparative metrics (MASE, WAPE) across models | Researcher, Officer |
| `GET` | `/api/v1/forecasting/explain` | Return TreeSHAP feature attributions for forecast | All |

---

### 2.6 Risk Intelligence (`/api/v1/risks`)

| Method | Endpoint | Description | Roles |
|---|---|---|---|
| `GET` | `/api/v1/risks/stockouts` | List medicines with projected stockout risks | All |
| `GET` | `/api/v1/risks/stockouts/{facility_id}/{medicine_id}` | Detailed risk profile, DSR, lead-time distribution | All |
| `GET` | `/api/v1/risks/expiries` | List batches with projected expiry waste (PUSE) | All |

---

### 2.7 Redistribution Optimization (`/api/v1/redistribution`)

| Method | Endpoint | Description | Roles |
|---|---|---|---|
| `POST` | `/api/v1/redistribution/optimize` | Trigger asynchronous MILP redistribution solver run | Admin, Officer |
| `GET` | `/api/v1/redistribution/recommendations` | List generated transfer proposals with status filters | All |
| `PATCH` | `/api/v1/redistribution/recommendations/{id}` | Accept, Reject, or Modify transfer recommendation | Admin, Officer, Manager |
| `GET` | `/api/v1/redistribution/voucher/{id}` | Export printable PDF transfer voucher | All |

---

### 2.8 Audit & System Health (`/api/v1/system`)

| Method | Endpoint | Description | Roles |
|---|---|---|---|
| `GET` | `/api/v1/system/audit-logs` | Query audit trail with user and entity filters | Admin, Auditor |
| `GET` | `/api/v1/system/health` | Service liveness and database connectivity check | Public |

---

## 3. Sample Request & Response Payloads

### 3.1 Run Redistribution Optimization (`POST /api/v1/redistribution/optimize`)

#### Request Payload:
```json
{
  "region_id": "REG-AMHARA-NORTH-SHEWA",
  "max_distance_km": 60.0,
  "donor_min_safety_days": 30,
  "priority_medicines_only": true,
  "weights": {
    "shortage_penalty": 10.0,
    "waste_penalty": 8.0,
    "transport_cost_per_km": 0.5
  }
}
```

#### Response Payload (`202 Accepted`):
```json
{
  "job_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "status": "QUEUED",
  "message": "Optimization solver task scheduled. Monitor status at /api/v1/redistribution/jobs/9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "estimated_completion_seconds": 8
}
```

---

### 3.2 Explainable Forecast Response (`GET /api/v1/forecasting/explain`)

#### Response Payload (`200 OK`):
```json
{
  "facility_id": "fac-001",
  "facility_name": "Debre Berhan Referral Hospital",
  "medicine_id": "med-amox-500",
  "medicine_name": "Amoxicillin 500mg Capsule",
  "model_name": "LightGBM-Regressor-v1.4",
  "forecast_horizon": "2026-12",
  "predicted_quantity": 4200.0,
  "confidence_interval_90": {
    "lower": 3850.0,
    "upper": 4620.0
  },
  "base_value": 3100.0,
  "shap_attributions": [
    {
      "feature": "seasonal_morbidity_index",
      "display_name": "Seasonal Respiratory Morbidity Spike",
      "shap_value": 650.0,
      "effect": "INCREASES_DEMAND"
    },
    {
      "feature": "lead_time_days_rolling_avg",
      "display_name": "EPSS Delivery Lead Time Extension",
      "shap_value": 320.0,
      "effect": "INCREASES_DEMAND"
    },
    {
      "feature": "historical_stockout_days_prior_month",
      "display_name": "Stockout De-censoring Adjustment",
      "shap_value": 240.0,
      "effect": "INCREASES_DEMAND"
    },
    {
      "feature": "ambient_temp_celsius",
      "display_name": "Local Ambient Temperature",
      "shap_value": -110.0,
      "effect": "DECREASES_DEMAND"
    }
  ],
  "plain_language_summary": "Forecasted demand is 35% higher than baseline, primarily driven by seasonal respiratory illness patterns and past-month stockout de-censoring."
}
```
