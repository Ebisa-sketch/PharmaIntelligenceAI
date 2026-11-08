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

### 1.1 Why this project?

Medicine shortages and pharmaceutical wastage can arise from several interacting problems:

- Incomplete, delayed, or inconsistent inventory records.
- Uncertain medicine consumption and changing demand.
- Delays between ordering and receiving supplies.
- Poor visibility of stock across facilities.
- Medicines remaining unused until their expiry dates.
- Limited information for comparing shortage risks and potential redistribution options.

A conventional inventory application primarily records and displays transactions. PharmaIntelligence AI aims to investigate how reliable data, predictive analysis, and constrained optimization can support better decisions.

### 1.2 Important positioning

Ethiopia already has pharmaceutical information and logistics initiatives, including Dagu and ForLab+. This project must not claim to replace them or assume that their APIs or data exports are publicly available.

PharmaIntelligence AI is proposed as a research and decision-support prototype that can work with authorized data imports and, if permission and technical access are later established, investigate interoperability.

Demand forecasting alone is not the claimed research novelty. Existing Ethiopian research has already investigated pharmaceutical forecasting using statistical and machine-learning methods. The project will investigate the integrated use of data-quality assessment, uncertainty-aware risk estimation, batch-level expiry analysis, explainable recommendations, and constrained redistribution. Any novelty claim must be supported by a systematic literature review.

---

## 2. Vision, Mission, and Purpose

### 2.1 Vision

To demonstrate how reliable data engineering and explainable AI can support more informed pharmaceutical inventory decisions in resource-constrained healthcare supply chains.

### 2.2 Mission

To design, implement, and evaluate a secure, modular, and explainable decision-support platform that analyses pharmaceutical inventory information and produces useful, reviewable risk assessments and recommendations.

### 2.3 Main purpose

The purpose is not simply to create another pharmacy management application. The purpose is to research and build an intelligent decision-support layer that can:

- Identify unreliable data before it is used by analytical models.
- Estimate future medicine requirements.
- Detect potential stockout situations early.
- Highlight batches with possible expiry-related wastage.
- Identify possible stock redistribution opportunities.
- Explain why a prediction or recommendation was produced.
- Evaluate whether AI-assisted decisions improve simulated outcomes compared with transparent baseline methods.

### 2.4 Intended users

The proposed users are:

- **System administrator:** manages system configuration, users, and access.
- **Facility pharmacy manager:** reviews facility inventory, batches, forecasts, and risks.
- **Regional supply-chain manager:** reviews aggregated facility-level risks and possible transfers, subject to authorized access.
- **Data analyst / researcher:** imports datasets, assesses data quality, runs experiments, and evaluates models.
- **Auditor:** reviews authorized records, decisions, approvals, and audit trails.

These roles are proposed for the prototype. Actual role definitions must be validated with relevant stakeholders.

---

## 3. Problem Statement

Healthcare facilities need dependable information to maintain medicine availability while avoiding unnecessary pharmaceutical wastage. Decisions can be difficult when inventory records are incomplete or inconsistent, medicine consumption is uncertain, supply lead times vary, and stock information is not sufficiently visible across facilities.

Although existing systems support pharmaceutical inventory and logistics activities, there remains a research and engineering opportunity to investigate how data reliability, predictive risk analysis, and constrained redistribution recommendations can be brought together in an explainable decision-support workflow.

This project proposes an integrated system that assesses inventory-data quality, forecasts medicine demand, estimates stockout and batch-expiry risks, and recommends feasible inter-facility redistribution for human review.

The project will first investigate the availability, suitability, licensing, and limitations of relevant datasets. If authorized real-world facility data cannot be obtained, synthetic data and suitable published research datasets will be used for development and controlled experiments. Results from synthetic data will not be represented as proof of real-world effectiveness.

---

## 4. Objectives

### 4.1 General objective

To design, develop, and evaluate an explainable AI-based pharmaceutical decision-support system for improving medicine availability and reducing avoidable pharmaceutical wastage in Ethiopian healthcare facilities.

### 4.2 Specific objectives

1. Review relevant literature and existing pharmaceutical information systems.
2. Identify and assess suitable pharmaceutical supply-chain datasets.
3. Design data-quality checks for missing, inconsistent, duplicated, delayed, and anomalous inventory records.
4. Develop and compare appropriate medicine demand forecasting methods.
5. Estimate medicine stockout risk using inventory, demand, and replenishment information.
6. Assess batch-level expiry risk using expiry dates, quantities, and projected consumption.
7. Formulate a constrained optimization model for potential medicine redistribution.
8. Provide understandable explanations, evidence, and uncertainty information for predictions and recommendations.
9. Develop a secure web application for authorized users.
10. Evaluate analytical performance and compare baseline decisions with AI-assisted decisions under clearly stated experimental conditions.

### 4.3 Research questions

- RQ1: How can pharmaceutical inventory-data quality be assessed before analytical modelling?
- RQ2: Which forecasting methods perform best for the available medicines and data conditions?
- RQ3: How accurately can future stockout risk be estimated using available stock, projected demand, and replenishment information?
- RQ4: How can batch-level expiry risk be assessed using expiry dates and projected consumption?
- RQ5: Under what constraints can redistribution recommendations reduce simulated shortage and expiry outcomes?
- RQ6: How can explanations and uncertainty information help users interpret and review system recommendations?

---

## 5. Scope

### 5.1 Included in the initial project

- Authorized CSV or spreadsheet data import.
- Data validation, cleaning support, and data-quality reporting.
- Medicine and facility reference information.
- Inventory transaction and batch records.
- Demand forecasting experiments.
- Stockout-risk estimation.
- Deterministic and forecast-assisted expiry-risk assessment.
- Redistribution optimization and simulation.
- Explainability and uncertainty presentation.
- Role-based access control and audit logging.
- Model evaluation, experiment tracking, and technical documentation.

### 5.2 Excluded from the initial project

- Replacing Dagu, ForLab+, or other official systems.
- Assuming access to private government databases or undocumented APIs.
- Automatically ordering, purchasing, transferring, or dispensing medicines.
- Patient diagnosis, prescribing, treatment recommendations, or clinical decision-making.
- Processing patient-identifiable health information.
- Claiming national-scale deployment or proven reduction in medicine shortages without a properly authorized real-world evaluation.
- Making automatic changes to source inventory records based on model predictions.

### 5.3 Initial pilot target

The following is a planning target, not confirmed data availability:

- 2–5 facilities, if facility-level data can be lawfully obtained.
- 10–20 selected medicines.
- Ideally 24–36 months of historical records.
- Monthly data if monthly observations are what the source provides.
- Batch and expiry information for expiry experiments.
- Replenishment and delivery information for stockout-risk experiments.
- Transfer information, or explicitly simulated transfer scenarios, for redistribution experiments.

The project scope must be reduced or adapted if the available dataset is smaller.

---

## 6. Stakeholders and Assumptions

### 6.1 Potential stakeholders

- Public healthcare facilities.
- Hospital and health-centre pharmacy personnel.
- Regional health and pharmaceutical supply-chain personnel.
- Ethiopian Pharmaceuticals Supply Service (EPSS).
- Ministry of Health and relevant digital-health stakeholders.
- University supervisor and academic reviewers.
- Researchers who publish relevant pharmaceutical supply-chain datasets.

### 6.2 Current project assumptions

- Direct healthcare data access is not currently available.
- The initial research scope is any accessible Ethiopian or relevant research dataset.
- Publicly available datasets may not contain all required fields.
- Synthetic data will be needed for application development and some controlled experiments.
- Data access, use, sharing, and publication must follow the source's permission, ethics, privacy, and licensing conditions.
- The prototype will use data imports initially rather than assume integration with existing national systems.

---

## 7. Data Requirements and Acquisition Strategy

Data availability is the project's most important early feasibility risk. Data acquisition and dataset inspection must happen before finalizing model choices.

### 7.1 Data source priorities

1. **Published research datasets:** inspect associated repositories, supplementary files, and data availability statements.
2. **Research author requests:** request access to relevant datasets and clarify terms of academic use.
3. **Official public resources:** investigate EPSS, Ministry of Health, and other official publications or datasets.
4. **Authorized facility data:** approach a healthcare facility or university contact for permission to use anonymized, aggregated inventory data.
5. **Synthetic data:** generate controlled data for software development and experiments where genuine records are unavailable.

Useful starting points to investigate:

- EPSS: https://epss.gov.et/
- Ethiopian Ministry of Health: https://moh.gov.et/
- Dagu portal: https://daguportal.moh.gov.et/
- Ministry of Health Master Facility Registry developer information: https://mfrpublic.moh.gov.et/developers

These links are research starting points, not confirmation that a particular dataset or API is publicly accessible.

### 7.2 Required data domains

| Data domain | Important fields | Main use |
|---|---|---|
| Medicine reference | medicine ID, name, strength, dosage form, unit, category | Consistent medicine identification |
| Facility reference | facility ID, type, region, location | Facility-level analysis |
| Consumption | medicine, facility, date/period, quantity issued | Demand analysis |
| Inventory snapshots | opening stock, closing stock, date | Stock position and reconciliation |
| Transactions | type, quantity, date, reference | Inventory reconstruction |
| Receipts | received quantity, receipt date, supplier/source | Supply history |
| Purchase/requisition | order date, quantity, expected date | Replenishment information |
| Deliveries | delivery date, quantity, order reference | Lead-time analysis |
| Batch information | batch ID, medicine, received date, expiry date, quantity | Expiry-risk assessment |
| Transfers | source facility, destination facility, quantity, dates | Redistribution analysis |
| Data provenance | source, extraction date, units, transformations | Reproducibility and trust |

Not every dataset will contain every domain. Each model must use only fields that are genuinely available and valid.

### 7.3 Data protection requirements

- Do not collect patient names, patient identifiers, diagnoses, or other patient-identifiable information.
- Use aggregated pharmacy and inventory data wherever possible.
- Obtain written authorization before using non-public facility records.
- Follow data-use agreements, institutional ethics requirements, and applicable law.
- Do not upload restricted records to public Git repositories or unapproved third-party services.
- Document data ownership, license, access restrictions, retention, and permitted publication.

### 7.4 Synthetic data policy

Synthetic data may be used to:

- Build and test import workflows.
- Test database relationships and application screens.
- Create controlled missing values and inventory inconsistencies.
- Simulate supply delays, demand variation, batch expiry, and transfers.
- Test optimization constraints and software behaviour.

Synthetic data must be labelled as synthetic. Model performance on synthetic data must not be described as validated real-world performance. Synthetic data must not be used to claim actual Ethiopian facility shortage rates or medicine demand patterns.

### 7.5 Dataset acceptance checklist

Before using a dataset, record:

- Source and owner.
- License and permitted use.
- Whether the dataset is real, aggregated, simulated, or synthetic.
- Observation period and frequency.
- Number of facilities and medicines.
- Missingness and data-quality limitations.
- Units and medicine identifiers.
- Whether stockout periods can be identified.
- Whether batch and expiry fields exist.
- Whether replenishment lead times exist.
- Whether the dataset can support each planned experiment.

---

## 8. Functional Requirements

Functional requirements describe what the system must do.

### FR-01: User authentication

- Users shall be able to sign in securely.
- Administrators shall be able to manage authorized accounts.
- The system shall enforce role-based permissions.

### FR-02: Facility and medicine reference management

- Authorized users shall be able to view relevant facility and medicine reference information.
- Medicine identifiers and units shall be validated.
- Duplicate or conflicting reference records shall be flagged.

### FR-03: Data import

- Authorized users shall be able to import supported CSV files.
- The system shall validate required columns, types, dates, units, and identifiers.
- Invalid rows shall be reported with understandable reasons.
- The system shall preserve import provenance.
- Re-importing a file shall not silently duplicate transactions.

### FR-04: Data quality assessment

- The system shall detect missing, duplicated, inconsistent, and anomalous records.
- It shall check stock reconciliation where the required transaction data exist.
- It shall display data-quality summaries and issue details.
- It shall not silently rewrite source data.

### FR-05: Inventory and batch visibility

- Authorized users shall be able to inspect available inventory information.
- The system shall display batch quantities and expiry dates where provided.
- The system shall distinguish original inventory records from calculated indicators and predictions.

### FR-06: Demand forecasting

- Authorized users shall be able to run supported forecasting experiments.
- The system shall display forecast horizons, units, model versions, and evaluation information.
- Forecasts shall include uncertainty information when the selected method supports it.
- Forecast outputs shall identify data limitations.

### FR-07: Stockout-risk analysis

- The system shall estimate stockout risk only when the necessary inventory, demand, and replenishment fields are available.
- It shall display risk level, estimated time or horizon, and contributing factors.
- It shall not present a probability as certainty.
- It shall flag cases where the input data are insufficient.

### FR-08: Expiry-risk analysis

- The system shall identify batches approaching expiry.
- It shall estimate potential unused quantities using clearly documented assumptions.
- It shall distinguish a date-based warning from a model-based risk estimate.

### FR-09: Redistribution recommendations

- The system shall identify possible donor and recipient facilities using eligible data.
- It shall consider medicine compatibility, expiry, minimum stock, projected demand, transport constraints, and storage constraints where available.
- It shall explain why a transfer is recommended.
- Recommendations shall require authorized human approval.
- The system shall not execute physical transfers automatically.

### FR-10: Explainability

- The system shall display important factors influencing supported predictions.
- Explanations shall be appropriate to the model and not imply causation without evidence.
- The system shall identify model version and data timestamp.

### FR-11: Reporting

- Authorized users shall be able to view and export permitted reports.
- Reports shall distinguish observations, forecasts, predictions, and recommendations.
- Reports shall include relevant dates, units, and limitations.

### FR-12: Audit trail

- The system shall record relevant imports, administrative changes, recommendation reviews, and approvals.
- Audit records shall include actor, action, timestamp, and relevant reference.
- Audit records shall be protected from unauthorized modification.

### FR-13: Model experiment management

- Researchers shall be able to record model configuration, dataset version, experiment dates, and metrics.
- The system shall retain enough information to reproduce reported experiments.

---

## 9. Non-Functional Requirements

### NFR-01: Security

- Use secure password hashing and protected sessions.
- Enforce server-side authorization for every protected operation.
- Isolate facility-level records according to the user's permissions.
- Protect secrets using environment variables or a secrets manager.
- Use encrypted connections in deployed environments.
- Validate and restrict data imports and exports.
- Maintain audit records for sensitive actions.

### NFR-02: Privacy and responsible use

- Minimize data collection.
- Avoid patient-identifiable data.
- Respect dataset licenses and access agreements.
- Do not expose one facility's restricted records to another.
- Require human approval for operational recommendations.

### NFR-03: Reliability

- Validate inputs before processing.
- Handle missing and invalid data explicitly.
- Avoid presenting predictions when required input data are unavailable.
- Preserve original source data and transformation history.

### NFR-04: Performance

- Support asynchronous processing for computationally expensive experiments.
- Avoid blocking normal application requests during model training.
- Define measurable performance targets after the dataset and deployment environment are known.

### NFR-05: Maintainability

- Use modular frontend, backend, data, and model components.
- Use documented API contracts.
- Apply automated tests and code-quality checks.
- Keep configuration separate from application code.

### NFR-06: Usability and accessibility

- Use clear labels, units, explanations, and status indicators.
- Avoid relying on colour alone to communicate risk.
- Make error messages actionable.
- Design for desktop use initially, with responsive layouts.

### NFR-07: Reproducibility

- Version datasets, code, model configurations, and experiments.
- Record random seeds where relevant.
- Use chronological evaluation splits for time-series experiments.
- Document preprocessing and feature-generation steps.

---

## 10. AI and Analytical Components

The project should not force every feature to use deep learning. Each analytical task should use a method appropriate to its data and purpose.

### 10.1 Component A: Data Quality Intelligence

**Purpose:** determine whether source records are sufficiently complete and consistent for analysis.

Potential techniques:

- Rule-based validation.
- Missing-value and duplicate detection.
- Inventory reconciliation.
- Interquartile-range checks.
- Isolation Forest for selected anomaly-detection experiments.

Example stock reconciliation:

`Expected closing stock = Opening stock + Receipts - Issues + Adjustments`

The exact formula must account for the source system's transaction definitions and units.

**Evaluation:** detection precision, recall, false-positive rate, missingness, and reconciliation error where ground truth is available.

### 10.2 Component B: Medicine Demand Forecasting

**Purpose:** estimate future consumption at the time frequency supported by the data.

Candidate baselines and models:

- Naive and seasonal-naive forecasts.
- Moving averages.
- ARIMA / SARIMA where appropriate.
- Croston or TSB for intermittent demand.
- Random Forest.
- XGBoost.
- LSTM as an optional deep-learning comparison if the data volume and sequence structure justify it.

Potential input variables:

- Historical medicine issues or consumption.
- Calendar and seasonal features.
- Facility and medicine attributes.
- Supply and stockout indicators where available.
- Other valid contextual variables supported by the dataset.

**Important modelling issue:** low recorded issues during a stockout may reflect unavailable stock rather than low underlying demand. This stockout-censoring problem must be investigated.

**Evaluation:** MAE, RMSE, WAPE, and MASE where suitable. Compare all candidate models with transparent baselines. Use prediction intervals or other uncertainty estimates when supported.

### 10.3 Component C: Stockout Risk Intelligence

**Purpose:** estimate the likelihood that usable stock will be exhausted before replenishment.

Potential features:

- Current usable stock.
- Demand forecast.
- Expected replenishment quantity.
- Estimated lead time.
- Open orders.
- Safety-stock policy.
- Historical supply delays.

Candidate methods:

- Rule-based inventory baseline.
- Logistic regression.
- Random Forest.
- XGBoost.
- Survival analysis as a later research extension.

**Evaluation:** precision, recall, F1, PR-AUC, calibration, and false-alarm rate. Class imbalance must be considered.

A stockout-risk model cannot be evaluated properly if stockout events or reliable proxy labels cannot be established.

### 10.4 Component D: Expiry Risk Intelligence

**Purpose:** estimate whether medicine batches may remain unused when their expiry dates are reached.

Start with transparent calculations:

- Remaining shelf life.
- Batch quantity.
- Projected consumption.
- Other eligible stock and FEFO allocation.
- Transfer eligibility and lead time where available.

The system should distinguish:

- A batch that is simply approaching expiry.
- A batch with a projected unused quantity.
- A batch with a model-estimated probability of expiry-related wastage.

Begin with deterministic calculations. Add machine learning only if sufficient labelled data and a clear evaluation strategy exist.

### 10.5 Component E: Redistribution Optimization

**Purpose:** identify feasible transfers from eligible donor facilities to facilities with projected shortages.

Possible optimization tools:

- Google OR-Tools.
- Pyomo.

Potential objective:

Minimize a weighted combination of:

- Expected shortage penalty.
- Expected expiry/wastage penalty.
- Transfer quantity or transport cost.
- Operational handling cost.

Potential constraints:

- Same compatible medicine and unit.
- Donor facility retains required minimum stock.
- Batch remains valid through the expected transfer/use period.
- Recipient has a projected need.
- Transfer quantity does not exceed eligible stock.
- Transport time, distance, and cost constraints where reliable data exist.
- Storage capacity and local policy constraints where available.

Weights and constraints must be documented and tested with stakeholders. Optimization results are recommendations, not authorization to move medicines.

### 10.6 Explainable AI

Potential methods include:

- SHAP for supported tree-based models.
- Feature importance.
- Transparent rule explanations.
- Sensitivity analysis.
- Confidence or uncertainty intervals where supported.

An explanation should tell the user which input factors influenced a prediction, not claim that those factors caused the outcome.

---

## 11. Experimental Design and Evaluation

### 11.1 Dataset splitting

For time-dependent data, use chronological splits rather than random row splitting.

A possible example, if sufficient history exists:

- Earliest 24 months: training.
- Next 6 months: validation.
- Latest 6 months: test.

Use rolling-origin backtesting where appropriate. The exact split depends on the available observation period.

If multiple facilities exist, consider additional evaluation on facilities not used for training to examine generalization.

### 11.2 Baseline comparisons

Every advanced model should be compared with an appropriate baseline.

| Task | Baseline | Candidate approaches |
|---|---|---|
| Data quality | Validation rules | Statistical checks, Isolation Forest |
| Forecasting | Naive / seasonal naive | ARIMA, Croston, Random Forest, XGBoost, optional LSTM |
| Stockout risk | Inventory threshold rules | Logistic regression, Random Forest, XGBoost |
| Expiry risk | Date and FEFO calculations | Forecast-assisted risk estimation |
| Redistribution | No transfer / simple rule | OR-Tools or Pyomo optimization |

### 11.3 Integrated decision simulation

Compare:

- Traditional inventory rules.
- Forecast-assisted inventory decisions.
- Forecast and stockout-risk decisions.
- Forecast, expiry, and redistribution-assisted decisions.

Possible outcome measures:

- Simulated stockout days.
- Simulated shortage quantity.
- Simulated expired units.
- Estimated wastage value, if defensible cost data exist.
- Emergency replenishment frequency.
- Transfer quantity and cost.
- Constraint violations.

All simulated outcomes must be labelled as simulations. They do not prove actual reductions in Ethiopian healthcare facilities.

### 11.4 Research reporting

For every experiment, record:

- Research question.
- Dataset source and version.
- Inclusion and exclusion rules.
- Preprocessing steps.
- Features.
- Model and hyperparameters.
- Training and test periods.
- Metrics and confidence/uncertainty information.
- Limitations and reproducibility instructions.

---

## 12. Proposed Technology Stack

| Layer | Proposed technology | Responsibility |
|---|---|---|
| Frontend | Next.js, React, TypeScript | Web application |
| UI | Tailwind CSS, shadcn/ui | Interface components |
| Backend | Python, FastAPI, Pydantic | API and business logic |
| Database | PostgreSQL | Structured application data |
| Data processing | Pandas, NumPy | Import, validation, transformation |
| Machine learning | Scikit-learn, XGBoost | Classical ML |
| Deep learning | PyTorch | Optional deep-learning experiments |
| Forecasting | Statsmodels | Statistical forecasting |
| Explainability | SHAP | Model explanations |
| Optimization | OR-Tools / Pyomo | Redistribution optimization |
| Experiment tracking | MLflow | Experiment and model tracking |
| Data versioning | DVC, where useful | Dataset versioning |
| Background jobs | Celery and Redis, later if needed | Long-running jobs |
| Testing | Pytest, frontend test tools | Automated testing |
| Version control | Git and GitHub | Source control |
| Packaging | Docker | Reproducible services |
| Deployment | Selected hosting after feasibility review | Application delivery |

The stack is a proposal, not a requirement to install every tool immediately. Prefer a smaller working architecture over unnecessary infrastructure.

---

## 13. Proposed System Architecture

### 13.1 Logical architecture

```text
                 AUTHORIZED USERS
                        |
                        v
              NEXT.JS WEB FRONTEND
                        |
                        v
                FASTAPI APPLICATION
             /          |           \
            /           |            \
           v            v             v
     DATA SERVICES   AI SERVICES   OPTIMIZATION
           |            |             |
           |            v             |
           |       MODEL OUTPUTS      |
           |            |             |
           +------------+-------------+
                        |
                        v
                  POSTGRESQL
                        |
                        v
             AUDIT / EXPERIMENT RECORDS
```

### 13.2 Architectural principles

- Keep the frontend separate from the backend API.
- Keep data-processing and ML code modular.
- Separate original records from derived features, predictions, and recommendations.
- Store model and dataset provenance.
- Enforce authorization on the server.
- Do not allow predictions to overwrite source inventory.
- Run long experiments outside ordinary request-response paths.
- Introduce background workers only when needed.

---

## 14. Application Modules and Screens

### 14.1 Executive Dashboard

- Overall inventory indicators.
- Medicines with high estimated stockout risk.
- Batches approaching expiry.
- Data-quality summary.
- Forecast overview.
- Pending recommendations.

### 14.2 Inventory Management

- Medicine reference information.
- Facility inventory snapshots.
- Inventory transactions.
- Batch and expiry records.
- Import history.

### 14.3 Data Quality Center

- Missing and duplicate records.
- Invalid dates and units.
- Stock reconciliation differences.
- Anomaly review.
- Data completeness and reliability indicators.

### 14.4 Forecasting Center

- Medicine and facility selection.
- Forecast horizon.
- Model selection and comparison.
- Forecast plots and uncertainty.
- Backtesting results.

### 14.5 Stockout Intelligence

- Estimated risk by medicine and facility.
- Expected time to shortage where supportable.
- Replenishment assumptions.
- Contributing factors.
- Data limitations.

### 14.6 Expiry Prevention Center

- Batch expiry timeline.
- Remaining shelf life.
- Projected batch consumption.
- Potential unused quantity.
- FEFO-based warnings.

### 14.7 Redistribution Center

- Potential donor facilities.
- Potential recipient facilities.
- Suggested medicine and quantity.
- Constraints and costs.
- Explanation and approval workflow.

### 14.8 AI Model Laboratory

- Dataset versions.
- Experiment configurations.
- Model metrics.
- Baseline comparisons.
- Model versions.
- Reproducibility information.

### 14.9 Administration and Audit

- Users and roles.
- Facility access policies.
- Import permissions.
- Audit events.
- System configuration.

---

## 15. Initial Database Design

The database will be normalized and designed around clear ownership and relationships. Final schema decisions will follow the verified dataset and SRS.

### 15.1 Core entities

| Entity | Purpose |
|---|---|
| users | User accounts |
| roles | Role definitions |
| permissions | Permission definitions |
| user_roles | User-role assignments |
| facilities | Facility reference information |
| medicines | Medicine reference information |
| medicine_categories | Medicine classifications |
| inventory_snapshots | Recorded stock at a point in time |
| inventory_transactions | Receipts, issues, and adjustments |
| medicine_batches | Batch quantities and expiry dates |
| suppliers | Supplier reference data, if available |
| requisitions | Requests for stock |
| purchase_orders | Order information, if available |
| deliveries | Delivery and lead-time records |
| data_imports | Import provenance |
| data_quality_issues | Data-quality findings |
| forecasts | Forecast outputs |
| stockout_predictions | Stockout-risk outputs |
| expiry_predictions | Expiry-risk outputs |
| redistribution_recommendations | Proposed transfers |
| redistribution_approvals | Human review and approval |
| model_versions | Model metadata |
| model_experiments | Experiment configuration and metrics |
| prediction_logs | Prediction provenance |
| audit_logs | Security and operational audit events |

### 15.2 Data separation

Keep these categories separate:

1. **Source observations:** imported or authorized records.
2. **Processed data:** validated and transformed analytical records.
3. **Model outputs:** forecasts, risk estimates, and scores.
4. **Recommendations:** proposed actions.
5. **Approvals and actions:** human-reviewed decisions and recorded outcomes.

A prediction must never silently change the original inventory record.

---

## 16. Security, Privacy, and Governance

Security is a core requirement, not a final polishing task.

- Enforce role-based access control.
- Apply facility-level data isolation.
- Check authorization on every protected backend operation.
- Hash passwords using a suitable password-hashing algorithm.
- Protect authentication sessions and secrets.
- Validate file imports and restrict dangerous file handling.
- Log sensitive administrative and approval operations.
- Protect backups and deployed database connections.
- Limit exports to authorized users.
- Do not expose restricted data through model logs or error messages.
- Require human review for operational recommendations.
- Document model limitations, data bias, and uncertainty.

No public deployment should contain real restricted facility data unless the necessary permissions and security controls are established.

---

## 17. Proposed Repository Structure

```text
PharmaIntelligenceAI/
│
├── README.md
├── .gitignore
├── .env.example
├── docker-compose.yml
│
├── docs/
│   ├── 01-project-proposal.md
│   ├── 02-problem-statement.md
│   ├── 03-literature-review.md
│   ├── 04-software-requirements-specification.md
│   ├── 05-system-architecture.md
│   ├── 06-database-design.md
│   ├── 07-dataset-specification.md
│   ├── 08-ai-experiment-plan.md
│   ├── 09-data-governance.md
│   └── 10-testing-and-evaluation.md
│
├── data/
│   ├── README.md
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   └── synthetic/
│
├── research/
│   ├── literature/
│   ├── notebooks/
│   ├── experiments/
│   └── results/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── repositories/
│   │   └── main.py
│   ├── tests/
│   └── requirements.txt
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── features/
│   ├── lib/
│   └── package.json
│
├── ml/
│   ├── data_quality/
│   ├── forecasting/
│   ├── stockout/
│   ├── expiry/
│   ├── redistribution/
│   ├── explainability/
│   ├── evaluation/
│   └── pipelines/
│
├── models/
│   ├── artifacts/
│   └── README.md
│
├── scripts/
│   ├── data/
│   ├── database/
│   └── experiments/
│
├── tests/
│   ├── integration/
│   └── end_to_end/
│
└── deployment/
    ├── docker/
    └── configuration/
```

This is the intended target structure. Directories will be created gradually as implementation begins. Do not commit private datasets, credentials, generated model artifacts, or large temporary files to Git by default.

---

## 18. Development Roadmap

A realistic initial planning estimate is approximately 16–22 weeks of part-time work. Actual duration depends heavily on data access, dataset quality, research requirements, and available time.

| Phase | Main activities | Expected output |
|---|---|---|
| 1. Research and feasibility | Literature review, system comparison, dataset investigation, data requests | Feasibility report and research proposal |
| 2. Requirements and design | SRS, architecture, data dictionary, database design | Approved design package |
| 3. Data engineering | Import pipeline, validation, synthetic data generator | Reproducible datasets and data pipeline |
| 4. AI experiments | Baselines, forecasting, stockout and expiry analysis | Evaluated model experiments |
| 5. Optimization | Redistribution constraints and simulation | Tested recommendation engine |
| 6. Backend | APIs, authentication, permissions, database integration | Working backend |
| 7. Frontend | Dashboard and analytical modules | Working web application |
| 8. Integration and testing | End-to-end tests, security checks, model integration | Integrated prototype |
| 9. Evaluation and documentation | Comparative experiments, limitations, final report | Research and portfolio release |

### 18.1 First-week plan

1. Create the repository and documentation folders.
2. Read and record relevant Ethiopian pharmaceutical research.
3. Inspect a promising published dataset and verify its license.
4. Prepare a dataset field inventory and data feasibility matrix.
5. Send a research-data request to relevant authors.
6. Draft the system requirements and architecture.
7. Decide the smallest scientifically defensible first experiment.

---

## 19. Testing Strategy

### 19.1 Software testing

- Unit tests for data validation and business rules.
- API tests for authentication and permissions.
- Database tests for relationships and constraints.
- Import tests for malformed and duplicate records.
- Integration tests for model-service interactions.
- End-to-end tests for important user workflows.
- Security tests for facility isolation and unauthorized access.

### 19.2 AI testing

- Chronological train/validation/test splits.
- Rolling-origin backtesting where appropriate.
- Baseline comparison.
- Data leakage checks.
- Missing-data sensitivity tests.
- Model calibration and uncertainty checks.
- Evaluation on unseen periods and, if possible, unseen facilities.

### 19.3 Optimization testing

- Verify every recommendation satisfies all hard constraints.
- Test no-surplus and no-demand cases.
- Test expired and soon-to-expire batches.
- Test insufficient transport or storage capacity.
- Compare optimization with simple rules.
- Record infeasible scenarios rather than silently relaxing constraints.

---

## 20. Risks and Mitigation

| Risk | Impact | Mitigation |
|---|---|---|
| No real facility data access | Limits real-world validation | Use published data and labelled synthetic experiments; continue authorized data requests |
| Dataset lacks batch records | Expiry model cannot be validated on real batches | Build deterministic synthetic batch scenarios; disclose limitation |
| Dataset lacks stockout labels | Stockout model cannot be evaluated reliably | Define defensible labels only where possible; otherwise report feasibility limits |
| Poor data quality | Unreliable model results | Profile data first and report quality limitations |
| Small dataset | Overfitting and weak generalization | Prefer simpler baselines and careful validation |
| Existing systems overlap | Weak project differentiation | Focus on explainable integrated decision support and evaluate the actual research gap |
| Unauthorized data use | Privacy and legal risk | Obtain permission and follow data-use conditions |
| Overly broad scope | Incomplete project | Deliver a small, evaluated vertical slice before expanding |
| Complex infrastructure | Delayed implementation | Start with a modular monolith and add services only when justified |

---

## 21. Definition of Success

The project will be considered technically successful when it can:

1. Import and validate a documented dataset.
2. Report data-quality issues without silently modifying source data.
3. Run and compare appropriate forecasting baselines and candidate models.
4. Estimate stockout risk when suitable labels and features exist.
5. assess batch expiry risk using valid batch and consumption information.
6. Generate redistribution recommendations that satisfy explicit constraints.
7. Explain model outputs and identify uncertainty and data limitations.
8. Enforce secure user and facility access.
9. Reproduce its experiments from documented data and code versions.
10. Present honest evaluation results, including negative results and limitations.

A successful prototype does not automatically demonstrate reduced real-world shortages. That claim would require a separately authorized and properly designed field evaluation.

---

## 22. Initial Research Deliverables

Before full implementation, prepare and review:

- Project proposal.
- Literature review and existing-system comparison.
- Research gap and contribution statement.
- Software Requirements Specification (SRS).
- Dataset specification and data dictionary.
- Data acquisition and governance plan.
- System architecture document.
- Database design.
- AI experiment and evaluation plan.
- Initial risk register.

These deliverables will be refined as the literature review and dataset inspection progress.

---

## 23. Immediate Next Steps

**Do these in order:**

1. Create the project directory and initialize Git.
2. Save this document as the root `README.md`.
3. Create a `docs/` directory for the detailed documents.
4. Inspect the published Ethiopian pharmaceutical forecasting dataset.
5. Verify its license, fields, observation period, and source.
6. Record which project components it can and cannot support.
7. Request additional research data where appropriate.
8. Finalize the first research experiment before implementing models.

### Initial project command sequence (Windows PowerShell)

```powershell
cd C:\Users\hp\Projects

mkdir PharmaIntelligenceAI
cd PharmaIntelligenceAI

git init
git branch -M main

mkdir docs, data, research, backend, frontend, ml, models, scripts, tests, deployment

mkdir data\raw, data\interim, data\processed, data\synthetic
mkdir research\literature, research\notebooks, research\experiments, research\results

New-Item README.md -ItemType File
New-Item .gitignore -ItemType File

git status
```

If you already created the project folders, do not repeat the `mkdir` commands; simply save this README in the existing project root.

---

## 24. Project Principles

1. **Evidence before claims:** research and dataset evidence must support project statements.
2. **Data before models:** inspect the dataset before selecting algorithms.
3. **Baselines before complexity:** compare advanced methods with simple, defensible alternatives.
4. **Explainability before automation:** predictions and recommendations must be understandable.
5. **Human oversight:** the platform supports authorized decisions; it does not execute medicine transfers automatically.
6. **Privacy by design:** avoid patient-identifiable information and protect restricted inventory records.
7. **Reproducibility:** retain data provenance, code versions, model configurations, and experiment results.
8. **Honest evaluation:** distinguish real, published, simulated, and synthetic data.
9. **Modular engineering:** build a maintainable application that can grow without unnecessary complexity.
10. **Real-world relevance:** every feature must address a documented problem or a validated user need.

---

## 25. Conclusion

PharmaIntelligence AI is intended to be a substantial applied research and software engineering project. Its value will come from the quality of its data, the defensibility of its experiments, the usefulness of its decision-support workflow, and the reliability of its implementation—not simply the number of AI algorithms or dashboard screens.

The first milestone is therefore not to train a neural network. It is to establish a credible research foundation, verify what data we can use, define the exact evaluation questions, and build a small reproducible data pipeline.

**Build carefully. Measure honestly. Explain every recommendation.**
