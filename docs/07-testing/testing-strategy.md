# Comprehensive Testing Strategy

---

## 1. Testing Philosophy and Quality Goals

PharmaIntelligence AI employs a multi-tiered verification framework to ensure mathematical correctness, system resilience, data security, and seamless user experience. 

Because inaccurate calculations or failed alerts in healthcare supply chains carry severe real-world consequences, testing is integrated directly into the CI/CD development pipeline:

```
┌────────────────────────────────────────────────────────┐
│                   TESTING PYRAMID                      │
├────────────────────────────────────────────────────────┤
│           End-to-End & Simulation Tests               │
│         Integration & Contract Tests (API/DB)          │
│       Data Ingestion & Mathematical Rule Tests         │
│     Unit Tests (Pytest, Vitest, Validation Logic)      │
└────────────────────────────────────────────────────────┘
```

---

## 2. Testing Levels and Tooling

### 2.1 Backend Unit & Logic Testing
- **Framework:** `pytest`, `pytest-cov`, `pytest-asyncio`.
- **Target Areas:**
  - Pydantic schema validation models (`schemas/`).
  - Ledger balance reconciliation formulas (`services/data_quality.py`).
  - Demand de-censoring calculations.
  - Days of Stock Remaining (DSR) and FEFO queue ordering logic.
  - OR-Tools constraint builders and penalty cost functions.
- **Coverage Mandate:** Minimum 85% line coverage across all service and calculation classes.

### 2.2 Integration and Database Testing
- **Tooling:** `pytest`, `testcontainers-python` (ephemeral PostgreSQL containers), `httpx.AsyncClient`.
- **Target Areas:**
  - Database repository CRUD methods and SQLAlchemy session management.
  - API endpoint authentication, JWT verification, and RBAC permission checks.
  - Multi-facility data isolation rules (ensuring facility users cannot access out-of-scope rows).
  - Multipart file upload parsing and transaction deduplication idempotency.

### 2.3 Machine Learning and Numerical Verification
- **Target Areas:**
  - Verification that time-series splits have zero future data leakage.
  - Deterministic evaluation of random seeds across ensemble models.
  - Invariance tests: verifying that scaling non-negative demand does not produce negative predictions.
  - Boundedness tests: verifying that predicted stockout probabilities $\hat{p} \in [0.0, 1.0]$.
  - Optimization feasibility tests: verifying that no recommended transfer ever breaches donor safety stock.

### 2.4 Frontend Verification
- **Framework:** Vitest, React Testing Library, Playwright for E2E.
- **Target Areas:**
  - Form validation and file upload drag-and-drop interactions.
  - State rendering for "Critical", "Warning", and "Safe" status badges.
  - Interactive chart rendering and drawer toggle behaviors.
  - Role-specific dashboard route protections.

---

## 3. Continuous Integration (CI) Workflow

Every Git commit and pull request triggers an automated GitHub Actions pipeline:
1. **Linting & Code Quality:** `ruff check`, `black --check`, `mypy` (backend); `eslint`, `prettier` (frontend).
2. **Automated Unit & Integration Tests:** Parallel execution of backend pytest suite and frontend Vitest suite.
3. **Database Migration Checks:** Automated test validating Alembic migrations upgrade and downgrade cleanly against a live PostgreSQL instance.
4. **Security Scan:** `bandit -r backend/`, `pip-audit`, `npm audit`.
