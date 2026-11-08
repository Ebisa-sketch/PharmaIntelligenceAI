# Software Requirements Specification (SRS)

## PharmaIntelligence AI: Decision-Support System for Pharmaceutical Inventory

---

## 1. Introduction

### 1.1 Purpose
This Software Requirements Specification (SRS) document provides a comprehensive description of the functional, non-functional, interface, and behavioral requirements for **PharmaIntelligence AI**. The intended audience includes software engineers, machine learning researchers, healthcare supply chain analysts, quality assurance testers, and project evaluators.

### 1.2 Document Conventions
- Requirements identifiers follow the standard format: `FR-XX` for Functional Requirements and `NFR-XX` for Non-Functional Requirements.
- Priority levels are defined using RFC 2119 keywords: **MUST** (mandatory for MVP), **SHOULD** (highly desirable), **MAY** (optional / future enhancement).

### 1.3 Intended Context
The platform is designed to operate as an intelligent analytical sidecar for Ethiopian public health facilities and regional health bureaus, ingesting inventory logs, verifying data integrity, generating de-censored demand forecasts, quantifying dual risks (stockout and expiry), optimizing lateral inventory transfers, and presenting transparent, explainable recommendations.

---

## 2. Overall Description

### 2.1 Product Perspective
PharmaIntelligence AI is a self-contained, modular, web-based software application consisting of:
- A responsive Next.js 14 frontend user interface.
- A Python FastAPI RESTful backend service layer.
- An analytical engine housing machine learning forecasting, risk classification, and OR-Tools optimization solvers.
- A PostgreSQL relational database with row-level security and audit logging.

```
┌────────────────────────────────────────────────────────┐
│                   CLIENT BROWSER                       │
│        (Next.js 14 / TypeScript / shadcn/ui)           │
└──────────────────────────┬─────────────────────────────┘
                           │ HTTPS / JSON REST API
┌──────────────────────────▼─────────────────────────────┐
│                 FASTAPI BACKEND CORE                   │
│      (Authentication, RBAC, Services, Repositories)     │
├───────────────┬────────────────────────┬───────────────┤
│ Data Quality  │ Machine Learning       │ Optimization  │
│ Engine        │ Pipeline               │ Engine        │
│ (Validation)  │ (Forecast/Risk/SHAP)   │ (OR-Tools)    │
└───────┬───────┴───────────┬────────────┴───────┬───────┘
        │                   │                    │
┌───────▼───────────────────▼────────────────────▼───────┐
│               POSTGRESQL RELATIONAL DB                 │
│  (Auth, Reference Data, Transactions, Model Outputs)   │
└────────────────────────────────────────────────────────┘
```

### 2.2 User Classes and Characteristics
1. **System Administrator:** IT or system lead responsible for user provisioning, facility onboarding, RBAC configuration, and audit review.
2. **Facility Pharmacy Manager:** Head of pharmacy at a hospital or health center managing stock on hand, reviewing expiry alerts, running local forecasts, and reviewing transfer requests.
3. **Regional Supply Chain Officer:** Regional Health Bureau or EPSS hub coordinator monitoring network-wide risks and approving lateral transfers.
4. **Data Analyst / Researcher:** Evaluates data quality, runs ML experiments, compares model baselines, and exports analytical findings.
5. **Auditor:** Inspects read-only logs of approvals, data provenance, and user activities for regulatory compliance.

### 2.3 Operating Environment
- **Server:** Linux (Ubuntu 22.04 LTS / Debian 12) or Docker Engine 24+, running Python 3.11+ and Node.js 20 LTS.
- **Client:** Modern standards-compliant web browsers (Chromium 100+, Firefox 100+, Safari 16+, Edge 100+).
- **Network Requirements:** Functional over low-bandwidth (256 kbps+) connections; supports offline CSV staging and asynchronous background processing.

---

## 3. External Interface Requirements

### 3.1 User Interfaces
- Modern, clean, accessible dashboard layout built with Tailwind CSS and shadcn/ui.
- High-contrast visual cues (avoiding red/green color blindness traps by pairing color indicators with descriptive text and icons).
- Modular views: Overview Dashboard, Inventory & Batches, Data Quality Center, Forecasting Center, Stockout Intelligence, Expiry Prevention, Redistribution Center, Model Laboratory, and Administration.

### 3.2 Hardware Interfaces
- No proprietary hardware interfaces required. Compatible with standard desktop PCs, laptops, and tablet browsers.

### 3.3 Software & Data Interfaces
- **File Ingestion:** Standard delimited CSV and Excel (.xlsx) file uploads.
- **API Interfaces:** RESTful OpenAPI 3.1-compliant endpoints providing JSON payloads.
- **Database Interface:** PostgreSQL 15+ connected via SQLAlchemy 2.0 ORM with Alembic migrations.

---

## 4. System Constraints and Design Guidelines
1. **Human-in-the-Loop:** Under no circumstances shall the system autonomously execute financial orders or commit lateral transfer dispatches without explicit human approval.
2. **Data Isolation:** Pharmacy managers must only view and modify records for their authorized facilities, while regional officers have aggregated regional view access.
3. **Preservation of Raw Provenance:** Automated cleaning rules and AI predictions MUST NOT overwrite original transaction values in the database.
