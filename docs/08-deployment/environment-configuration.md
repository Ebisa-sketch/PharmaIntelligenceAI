# Environment Configuration Reference

---

## 1. Overview and Security Principles

All configuration in PharmaIntelligence AI is managed through environment variables adhering to the **Twelve-Factor App methodology**. 

### Critical Rules:
1. **Never Commit Secrets:** Production passwords, encryption salts, and JWT secrets MUST NEVER be committed to Git.
2. **Template Maintenance:** All configuration variables must be documented in `.env.example` with clear descriptions and safe development defaults.

---

## 2. Configuration Parameters Catalog

### 2.1 General Application Settings

| Variable Name | Required | Default (Dev) | Description |
|---|---|---|---|
| `ENVIRONMENT` | Yes | `development` | Runtime mode: `development`, `staging`, `production` |
| `LOG_LEVEL` | No | `INFO` | Logging verbosity: `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `APP_SECRET_KEY` | Yes | `dev-insecure-secret-key-change-me` | Master cryptographic signing key |

---

### 2.2 PostgreSQL Database Settings

| Variable Name | Required | Default (Dev) | Description |
|---|---|---|---|
| `POSTGRES_SERVER` | Yes | `localhost` | Database hostname or container name |
| `POSTGRES_PORT` | No | `5432` | Database port |
| `POSTGRES_DB` | Yes | `pharmaintel_db` | Relational database name |
| `POSTGRES_USER` | Yes | `pharmaintel_user` | Database user account |
| `POSTGRES_PASSWORD` | Yes | `pharmaintel_password` | Database password |
| `DATABASE_URL` | Derived | `postgresql+asyncpg://...` | Full SQLAlchemy async connection URI |

---

### 2.3 Authentication and JWT Tokens

| Variable Name | Required | Default (Dev) | Description |
|---|---|---|---|
| `JWT_SECRET_KEY` | Yes | `dev-jwt-secret-replace-in-production` | Secret key used for signing JWT access tokens |
| `JWT_ALGORITHM` | No | `HS256` | Cryptographic signature algorithm (`HS256` or `RS256`) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | `60` | Lifespan of JWT access tokens in minutes |
| `REFRESH_TOKEN_EXPIRE_DAYS` | No | `7` | Lifespan of session refresh tokens in days |

---

### 2.4 CORS and Frontend Connectivity

| Variable Name | Required | Default (Dev) | Description |
|---|---|---|---|
| `BACKEND_CORS_ORIGINS` | Yes | `["http://localhost:3000"]` | JSON array of permitted frontend origins |
| `NEXT_PUBLIC_API_URL` | Yes | `http://localhost:8000/api/v1` | Backend REST endpoint for client browser calls |

---

### 2.5 Machine Learning & Optimization Engine

| Variable Name | Required | Default (Dev) | Description |
|---|---|---|---|
| `MODEL_ARTIFACTS_PATH` | No | `./models/artifacts` | Directory holding serialized `.joblib` model binaries |
| `MLFLOW_TRACKING_URI` | No | `http://localhost:5000` | MLflow tracking server URI (for experiments) |
| `SOLVER_TIMEOUT_SECONDS` | No | `10.0` | Maximum execution time for OR-Tools MILP solver |
| `MAX_TRANSFER_RADIUS_KM`| No | `75.0` | Maximum road distance permitted for lateral transfers |

---

## 3. Sample Development `.env` File

```bash
# Environment & Core
ENVIRONMENT=development
LOG_LEVEL=DEBUG
APP_SECRET_KEY=dev-secret-key-change-in-production

# PostgreSQL Database
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=pharmaintel_db
POSTGRES_USER=pharmaintel_user
POSTGRES_PASSWORD=pharmaintel_password

# Authentication
JWT_SECRET_KEY=dev-jwt-super-secret-key-2026!
ACCESS_TOKEN_EXPIRE_MINUTES=120
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS & Networking
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# Optimization & ML
SOLVER_TIMEOUT_SECONDS=10.0
MAX_TRANSFER_RADIUS_KM=75.0
```
