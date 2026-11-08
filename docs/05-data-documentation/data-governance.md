# Data Governance, Ethics, and Security Policy

---

## 1. Governance Principles and Ethical Mandate

PharmaIntelligence AI operates at the intersection of public health informatics and computational logistics. Recognizing the sensitivity of health system operational data, the platform is governed by strict ethical, legal, and operational principles:

1. **Patient Privacy by Design:** The system is exclusively an inventory, supply-chain, and logistics decision-support tool. It **never captures, ingests, or stores Protected Health Information (PHI)** or patient clinical histories.
2. **Institutional Stewardship:** Facility inventory records belong to the participating healthcare facilities, Regional Health Bureaus, and EPSS. The platform acts as an authorized processor, not an owner.
3. **Transparency and Accountability:** Algorithmic outputs never substitute for human authority. Every analytical model, baseline comparison, and recommendation must be explainable and auditable.
4. **Honest Scientific Evaluation:** Clear distinction between results generated from real-world empirical records versus synthetic benchmark data.

---

## 2. Data Protection and Multi-Tenancy Architecture

### 2.1 Multi-Facility Data Isolation
- Health facility users (`ROLE_PHARMACY_MANAGER`) are bound to their assigned facility via cryptographic JWT claims.
- PostgreSQL database queries enforce facility filtering at the repository layer. Direct queries spanning multiple facilities require regional or administrative authorization.

### 2.2 Anonymization & De-Identification
- When exporting research datasets for external academic benchmarking, facility identifiers and regional woredas must be pseudonymized (e.g., `FAC-001`, `FAC-002`) to prevent commercial exploitation or institutional stigmatization.

### 2.3 Cryptographic Integrity and Secrets Management
- All system passwords hashed using Argon2id or Bcrypt work factor 12.
- Production database credentials, JWT secret keys, and encryption salts must be injected via environment variables or secret managers (e.g., Docker secrets, HashiCorp Vault); secrets must NEVER be committed to Git repositories.

---

## 3. Data Lifecycle and Retention

| Phase | Policy / Handling Procedure |
|---|---|
| **Collection & Ingestion** | Authorized CSV/Excel upload via TLS 1.3 encrypted connection; schema and SHA-256 hash verified. |
| **Storage & Persistence** | PostgreSQL 15 relational tables with encrypted volume blocks (LUKS / AES-256). |
| **Model Ingestion** | ML models train on sanitized, de-censored data tables; raw transaction tables remain untouched. |
| **Archival & Retention** | Historical transaction ledgers retained for a minimum of 5 years to support longitudinal research; audit logs retained for 24 months. |
| **Disposal** | Deprecated datasets purged using cryptographically secure disk overwrites upon formal request from data owners. |

---

## 4. Compliance and Regulatory Alignment

The data governance policies of PharmaIntelligence AI are formulated to align with:
- **Ethiopian Data Protection Framework:** Proclamation on Personal Data Protection and Ministry of Health digital health guidelines.
- **EFDA Guidelines:** Ethiopian Food and Drug Authority standards for pharmaceutical storage, batch tracking, and recall management.
- **FAIR Data Principles:** Ensuring research artifacts produced by the system are **F**indable, **A**ccessible, **I**nteroperable, and **R**eusable where public licensing permits.
