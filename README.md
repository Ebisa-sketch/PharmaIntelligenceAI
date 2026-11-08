# PharmaIntelligence AI

## An Explainable AI-Based Decision-Support System for Pharmaceutical Stockout Risk, Expiry Prevention, and Inventory Redistribution in Ethiopian Healthcare Facilities

> **Project status:** Research and planning  
> **Project type:** Advanced AI / Machine Learning / Full-Stack Software Engineering / Applied Research  
> **Initial target context:** Ethiopian healthcare facilities  
> **Primary principle:** Build an evidence-based decision-support prototype that complements existing pharmaceutical information systems. It does not replace authorized clinical, pharmacy, procurement, or supply-chain decisions.

---

## 1. Project Overview

PharmaIntelligence AI is a proposed explainable AI-based pharmaceutical supply-chain decision-support platform. It is intended to help authorized healthcare and pharmaceutical supply-chain personnel understand inventory data, anticipate potential medicine shortages, identify batches at risk of expiry, and evaluate possible redistribution of available stock between facilities.

The project combines data engineering, statistical analysis, machine learning, explainable AI, optimization, and full-stack application development.

The platform is designed around five connected capabilities:

1. **Data Quality Intelligence** — assess the completeness, consistency, and reliability of pharmaceutical inventory records.
2. **Medicine Demand Forecasting** — estimate future medicine consumption using appropriate statistical and machine-learning methods.
3. **Stockout Risk Intelligence** — estimate the risk that usable stock will be exhausted before replenishment.
4. **Expiry Risk Intelligence** — identify batches that may expire before they can reasonably be consumed.
5. **Redistribution Optimization** — recommend feasible transfers from facilities with eligible surplus to facilities facing potential shortages.

The system will explain its predictions, display uncertainty and data limitations, and require human review before operational recommendations are approved.

---

## 2. Repository Structure

```text
PharmaIntelligenceAI/
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
├── .dockerignore
├── docker-compose.yml
├── Makefile
├── docs/                      # Project documentation (overview, research, requirements, etc.)
├── frontend/                  # Next.js web application (App router, shadcn/ui, Tailwind)
├── backend/                   # Python FastAPI backend (API, models, services, repositories)
├── ml/                        # AI & Machine learning pipelines, models, notebooks
├── optimization/              # Redistribution engine (OR-Tools, Pyomo solvers)
├── data/                      # Datasets, synthetic data, schemas, metadata
├── models/                    # Model registry and saved artifacts
├── research/                  # Academic experiments, literature, logs
├── scripts/                   # Setup, database seeding, data validation scripts
├── tests/                     # Unit, integration, e2e, and AI evaluation tests
├── deployment/                # Dockerfiles, Nginx, deployment configs
└── .github/                   # CI/CD workflows and PR templates
```

Please refer to `docs/` for comprehensive design specifications, research methodology, and documentation.
