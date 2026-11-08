# Non-Functional Requirements Specification

This document defines the quality attributes, constraints, performance benchmarks, and security mandates for PharmaIntelligence AI. Every requirement follows the standard `NFR-XX` identifier scheme.

---

## NFR-01: Security Requirements
- **NFR-01.1 (Encryption in Transit):** All client-to-server and inter-service HTTP communications MUST be encrypted using TLS 1.3 (minimum TLS 1.2).
- **NFR-01.2 (Encryption at Rest):** Database tables and file storage containing sensitive facility or operational logs MUST support AES-256 encryption at rest.
- **NFR-01.3 (Credential Security):** User passwords MUST be hashed using Argon2id or Bcrypt with a minimum work factor of 12. Plaintext passwords MUST NEVER be logged or stored.
- **NFR-01.4 (API Protection):** API endpoints MUST enforce rate limiting (e.g., 60 requests/minute per IP for general endpoints; 5 requests/minute for authentication endpoints) to prevent brute-force attacks.
- **NFR-01.5 (Input Sanitization):** All uploaded files, form inputs, and API query parameters MUST undergo strict input validation and sanitization to prevent SQL injection, Cross-Site Scripting (XSS), and path traversal attacks.

---

## NFR-02: Privacy and Data Governance
- **NFR-02.1 (No Patient Identifiable Data):** The platform MUST NEVER ingest, process, or store Protected Health Information (PHI) or Personally Identifiable Information (PII) of patients.
- **NFR-02.2 (Multi-Tenant Facility Isolation):** Facility users MUST be prevented from querying or viewing stock levels of other facilities unless granted cross-facility regional permissions.
- **NFR-02.3 (Data Retention and Purging):** Soft-delete mechanisms MUST be implemented for operational entities; raw audit logs MUST be retained for a minimum of 24 months for regulatory traceability.

---

## NFR-03: Reliability and Fault Tolerance
- **NFR-03.1 (High Availability):** The system architecture SHOULD achieve 99.5% operational uptime during standard business hours (8:00 AM – 6:00 PM EAT).
- **NFR-03.2 (Graceful Degradation):** If machine-learning forecasting or optimization microservices become unavailable, the frontend MUST gracefully fall back to displaying historical statistics and rule-based Days-of-Stock heuristics without crashing.
- **NFR-03.3 (Data Integrity and Atomic Transactions):** All database modifications involving multi-table operations (such as batch adjustments or transfer approvals) MUST execute within atomic database transactions (ACID compliance).

---

## NFR-04: Performance and Scalability
- **NFR-04.1 (API Response Times):** Standard REST API queries for dashboard metrics, inventory summaries, and risk lists MUST return in < 500 ms under a concurrent load of 50 active users.
- **NFR-04.2 (Asynchronous Heavy Processing):** Long-running computational tasks (e.g., training machine learning models, running MILP redistribution solvers across >50 facilities) MUST run asynchronously as background jobs.
- **NFR-04.3 (Import Throughput):** The data ingestion pipeline MUST process and validate a 10,000-row inventory transaction CSV in < 15 seconds.

---

## NFR-05: Maintainability and Extensibility
- **NFR-05.1 (Code Modularity):** The codebase MUST adhere to clean architectural separation (domain entities, repositories, service layer, API controllers).
- **NFR-05.2 (Type Safety & Documentation):** Backend Python code MUST utilize complete type annotations validated by MyPy and Pydantic v2; frontend code MUST use strict TypeScript mode.
- **NFR-05.3 (Automated Test Coverage):** Unit and integration test suites MUST achieve a minimum of 80% code coverage across core business logic, validation routines, and API endpoints.

---

## NFR-06: Usability and Human-Centered Design
- **NFR-06.1 (Accessibility & Color Blindness):** Status indicators MUST NOT rely solely on color. Red/Yellow/Green indicators MUST be accompanied by explicit text labels ("Critical", "Warning", "Safe") and distinct iconography.
- **NFR-06.2 (Cognitive Load & Explainability):** Complex algorithmic outputs MUST feature progressive disclosure: showing high-level risk summaries first, with expandable drawers for feature attributions (TreeSHAP) and mathematical bounds.
- **NFR-06.3 (Actionable Error Messaging):** Data import rejections MUST pinpoint exact file line numbers, column names, and human-readable error descriptions rather than technical database error strings.

---

## NFR-07: Reproducibility and Scientific Rigor
- **NFR-07.1 (Experiment Tracking):** All model training runs, hyperparameters, feature sets, and chronological split dates MUST be tracked via MLflow or reproducible JSON metadata.
- **NFR-07.2 (Deterministic Random Seeds):** All randomized algorithmic components (e.g., data splitting, tree ensemble training seeds) MUST use fixed seeds recorded in experiment configurations.
- **NFR-07.3 (Transparent Baselines):** All reported machine learning metrics MUST be directly benchmarked against established transparent baselines (Naive, Historical Average, SMA).
