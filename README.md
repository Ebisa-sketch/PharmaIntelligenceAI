# PharmaIntelligence AI

### An Explainable AI-Based Decision-Support System for Pharmaceutical Stockout Risk, Expiry Prevention, and Inventory Redistribution in Ethiopian Healthcare Facilities

[![Backend CI](https://github.com/Ebisa-sketch/PharmaIntelligenceAI/actions/workflows/backend-ci.yml/badge.svg)](https://github.com/Ebisa-sketch/PharmaIntelligenceAI/actions/workflows/backend-ci.yml)
[![Frontend CI](https://github.com/Ebisa-sketch/PharmaIntelligenceAI/actions/workflows/frontend-ci.yml/badge.svg)](https://github.com/Ebisa-sketch/PharmaIntelligenceAI/actions/workflows/frontend-ci.yml)
[![Test Suite](https://github.com/Ebisa-sketch/PharmaIntelligenceAI/actions/workflows/tests.yml/badge.svg)](https://github.com/Ebisa-sketch/PharmaIntelligenceAI/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 1. Executive Summary & Research Positioning

**PharmaIntelligence AI** is an explainable AI (XAI) clinical supply-chain decision-support prototype engineered to optimize essential medicine availability and eliminate avoidable expiry wastage across multi-tier public healthcare networks in Ethiopia (Tertiary Referral Hospitals, General Hospitals, and Primary Healthcare Units).

### Core Research Principle
> **Evidence-based decision-support prototype:** The system complements existing pharmaceutical logistics information systems (such as Dagu and ForLab+). It provides decision support and does **not** replace authorized clinical, pharmacy, procurement, or regulatory supply-chain decisions. All automated recommendations require human verification and tripartite approval before physical transfer execution.

---

## 2. The Five Core Clinical Decision Capabilities

```text
                               AUTHORIZED HEALTHCARE PERSONNEL
                                              |
                                              v
                                    NEXT.JS WEB FRONTEND
                       (36 Responsive Clinical & Analytical Modules)
                                              |
                                              v
                                     FASTAPI REST BACKEND
                 ┌────────────────────────────┼────────────────────────────┐
                 v                            v                            v
      DATA QUALITY INTELLIGENCE     PREDICTIVE AI ENGINES        CONSTRAINED OPTIMIZATION
        • 5D DQI Score (0-100)     • Syntetos-Boylan (ADI/CV²)   • Mixed-Integer LP (MILP)
        • Stock Reconciliation     • Stockout De-censoring       • Multi-facility Mesh
        • Anomaly Detection        • HistGradientBoosting / SBA  • Google OR-Tools / SCIP
        • Ledger Ingestion Center  • TreeSHAP Attribution        • Cold-Chain & Feasibility
                 │                            │                            │
                 └────────────────────────────┼────────────────────────────┘
                                              v
                                      SQL DATABASE / ORM
                         (Facilities, Inventories, Batches, Consignments)
```

1. **Data Quality Intelligence (DQI):** Multi-dimensional record assessment evaluating Completeness, Consistency, Timeliness, Validity, and Stock Reconciliation ($\text{Closing Stock} = \text{Opening} + \text{Receipts} - \text{Issues} + \text{Adjustments}$).
2. **Medicine Demand Forecasting:** Adaptive algorithm selection using Syntetos-Boylan categorization (ADI = 1.32, $\text{CV}^2 = 0.49$) across Smooth, Intermittent, Erratic, and Lumpy patterns, integrated with stockout de-censoring ($y_{\text{adj}} = y_{\text{obs}} / R$).
3. **Stockout Risk Intelligence:** Calibrated probabilistic early warning (AUC 0.967) estimating the likelihood that usable stock will be exhausted before replenishment delivery, explained via TreeSHAP feature attribution.
4. **Expiry Prevention Intelligence:** First-Expired First-Out (FEFO) batch-level velocity matching calculating Projected Under-Utilization (PUU) and salvaging expiring batches before disposal thresholds.
5. **Redistribution Optimization:** SCIP / Google OR-Tools Mixed-Integer Linear Programming (MILP) balancing multi-commodity logistics transfer costs against stockout penalties and expiring inventory salvage value.

---

## 3. Research Questions & Methodology Answers

| Research Question | Scientific Challenge | Implemented Methodology in PharmaIntelligence AI |
|---|---|---|
| **RQ1: Data Quality** | Unreliable, delayed, and non-reconciled pharmacy records | 5-Dimensional DQI Engine + automated ledger reconciliation and CSV pre-validation. |
| **RQ2: Demand Forecasting** | Intermittent dispensing & stockout-censored zeroes | Syntetos-Boylan classification (Croston-SBA + HistGradientBoosting) with in-stock ratio de-censoring ($R = \frac{T - S}{T}$). |
| **RQ3: Stockout Risk** | Static buffer rules fail during erratic epidemic spikes | Multi-feature Random Forest/HistGB classifier (AUC 0.967) estimating shortage probability prior to lead-time delivery. |
| **RQ4: Expiry Prevention** | Calendar-only alerts trigger high false alarms & waste | Batch shelf-life matched against de-censored consumption velocity ($PUU = \text{Batch Qty} - \text{Consumption to Expiry}$). |
| **RQ5: Redistribution** | Fragmented isolated facilities with high transport costs | Constrained MILP optimization with maximum radius bounds, cold-chain preservation, and tripartite waybills. |
| **RQ6: Explainability** | Black-box AI recommendations lack clinical trust | TreeSHAP cooperative game-theoretic attribution decomposing risk drivers into transparent Birr and unit factors. |

---

## 4. Key Application Modules & Screens

The web application provides 36 fully typed, production-ready routes:

- **Executive Console (`/dashboard`):** High-level KPIs, stockout risk distribution, regional inventory health, and live clinical alert feeds.
- **Data & Ledger Ingestion Center (`/inventory/import`):** Drag-and-drop CSV batch ingestion, pre-validation error detection, and format templates.
- **Inventory & NEML Catalog (`/inventory`, `/inventory/medicines`, `/inventory/batches`):** Real-time bin-card reconciliation, lot tracking, and days of stock remaining (DSR).
- **Demand Forecasting Center (`/forecasting`, `/forecasting/analysis`):** Multi-model backtesting, prediction intervals (P10, P50, P90), Syntetos-Boylan quadrant, and Stockout De-censoring Investigation.
- **Stockout Risk Intelligence (`/stockout-intelligence`):** Real-time risk scoring, Days of Stock Remaining (DSR), lead-time tracking, and interactive TreeSHAP explainability modals.
- **Expiry Prevention Center (`/expiry-prevention`):** FEFO prioritization queue, batch under-utilization analysis, and single-click Batch Lateral Transfer triggers.
- **Redistribution Optimization Center (`/redistribution`, `/redistribution/recommendations`, `/redistribution/approvals`):** Dynamic MILP optimization tuner, What-If Policy Simulation Lab (4-Policy Comparison Matrix), and Tripartite Clinical Consignment Notes (Waybills).
- **AI Model Laboratory (`/ai-laboratory`, `/ai-laboratory/models`, `/ai-laboratory/evaluation`, `/ai-laboratory/experiments`):** Enterprise Model Registry tracking production algorithms, hyperparameters, reproducibility seeds, and formal baseline comparison tables.
- **Reports & Clinical Exporter (`/reports`):** Multi-dataset clinical CSV exports (Inventory Health, Stockout Risk, Expiry Prevention, Transfer Audit) and printable Executive Dossier.
- **Alert Dispatch & Notifications (`/notifications`):** Real-time aggregated alert feed connecting stockout risks, expiring batches, and pending redistribution approvals.

---

## 5. Technology Stack

| Layer | Component | Version / Technology |
|---|---|---|
| **Frontend** | Framework | Next.js 14 (App Router), React 18, TypeScript |
| | Styling & UI | Tailwind CSS, Lucide Icons, Custom Accessible Components |
| | State & Fetching | React Hooks, Context API, Typed REST Client with Fallbacks |
| **Backend** | API Engine | FastAPI, Python 3.12, Pydantic v2 |
| | ORM & DB | SQLAlchemy 2.0, SQLite (Dev) / PostgreSQL (Production) |
| | Auth & Security | OAuth2 with JWT (Access + Refresh tokens), RBAC, Password Hashing |
| **AI / ML** | Time-Series & Regression | scikit-learn 1.4, Statsmodels, Custom Croston-Syntetos-Boylan |
| | Explainability (XAI) | TreeSHAP (Lundberg & Lee) Exact Game-Theoretic Attribution |
| | Mathematical Optimization | Google OR-Tools 9.8, SCIP Backend, PuLP MILP Solver |
| **Testing** | Backend Tests | Pytest (45/45 Unit, API, Integration, and Lifecycle Tests) |
| | Frontend Tests | Jest, React Testing Library, TypeScript Compiler (`tsc --noEmit`) |

---

## 6. Quick Start Guide

### Prerequisites
- Python 3.11 or 3.12
- Node.js 18+ and `pnpm`
- Git

### One-Click Launch (Windows PowerShell)
```powershell
# Clone the repository
git clone https://github.com/Ebisa-sketch/PharmaIntelligenceAI.git
cd PharmaIntelligenceAI

# Start both Backend (port 8000) and Frontend (port 3000) concurrently
.\run_dev.ps1
```

### Manual Setup

#### 1. Backend Setup
```powershell
# Navigate to backend and create virtual environment
cd backend
python -m venv ..\.venv
..\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Seed demonstration database with Ethiopian healthcare facilities
python -m app.management.generate_synthetic --facilities 6 --months 24 --seed-db

# Launch FastAPI server
uvicorn app.main:app --reload --port 8000
```
API Documentation will be live at: `http://localhost:8000/docs`

#### 2. Frontend Setup
```powershell
cd frontend

# Install packages
pnpm install

# Start Next.js development server
pnpm dev
```
Access the application dashboard at: `http://localhost:3000`

Default demo credentials:
- **Email:** `admin@pharmaintelligence.et`
- **Password:** `Admin@123456`

---

## 7. Verification & Automated Test Suites

The project features comprehensive end-to-end and unit testing pipelines:

```powershell
# 1. Run all 45 Backend Tests (Security, AI Models, Optimization, End-to-End Clinical Flow)
cd backend
..\.venv\Scripts\pytest.exe tests -v

# 2. Run Frontend TypeScript Static Analysis
cd frontend
pnpm type-check

# 3. Run Frontend Unit Tests
cd frontend
pnpm test

# 4. Compile Production Frontend Build
cd frontend
pnpm build
```

---

## 8. Research Deliverables & Documentation

Detailed academic specifications, software architecture, and research papers are available in the repository:
- Master Research Blueprint: [`PharmaIntelligenceAI_README.md`](PharmaIntelligenceAI_README.md)
- Software Requirements Specification (SRS): [`docs/04-software-requirements-specification.md`](docs/04-software-requirements-specification.md)
- System Architecture Design: [`docs/05-system-architecture.md`](docs/05-system-architecture.md)
- Database ERD & Schema Design: [`docs/06-database-design.md`](docs/06-database-design.md)
- AI Experiment Plan & Baselines: [`docs/08-ai-experiment-plan.md`](docs/08-ai-experiment-plan.md)
- Research Log: [`research/research-log.md`](research/research-log.md)

---

## 9. Ethics, Privacy & Responsible AI

1. **Synthetic & Aggregated Data Only:** All demonstration data in this repository are synthetic, statistically calibrated to published Ethiopian epidemiological patterns. No identifiable patient data or restricted government health records are stored.
2. **Clinical Decision Support:** Recommendations produced by the MILP solver and AI models are consultative and strictly subject to verification and sign-off by authorized pharmacy professionals.
3. **Transparency & Reproducibility:** Every AI model logs its feature attribution, confidence intervals, random seeds, and data limitations.
