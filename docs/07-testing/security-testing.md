# Security Testing and Vulnerability Assessment

---

## 1. Security Testing Strategy

Security in healthcare software is foundational. PharmaIntelligence AI is subjected to systematic vulnerability evaluations targeting the OWASP Top 10 API Security Risks, cryptographic standards, multi-tenant data boundaries, and audit trail integrity.

```
┌────────────────────────────────────────────────────────┐
│                   SECURITY TEST SUITE                  │
├──────────────────────────┬─────────────────────────────┤
│ 1. Static Analysis (SAST)│ Bandit, Ruff, Pip-Audit     │
│ 2. Dynamic Testing (DAST)│ OWASP ZAP, Postman Security │
│ 3. RBAC & Tenant Escapes │ Broken Object Level (BOLA)  │
│ 4. Cryptographic Audits  │ TLS 1.3, Argon2id, Secrets  │
└──────────────────────────┴─────────────────────────────┘
```

---

## 2. Targeted Threat Scenarios and Test Protocols

### 2.1 Broken Object Level Authorization (BOLA / IDOR)
- **Vulnerability Target:** A malicious pharmacy manager attempts to access or alter another clinic's inventory or transfer proposals by tampering with URL parameters (`/api/v1/inventory/batches?facility_id=<OTHER_FACILITY_UUID>`).
- **Test Protocol:** Automated test script authenticates as User A (scoped to Facility 1) and issues `GET`, `PATCH`, and `DELETE` requests against entities owned by Facility 2.
- **Pass Criteria:** Every cross-facility request MUST return HTTP 403 Forbidden.

### 2.2 SQL Injection (SQLi) & ORM Escapes
- **Vulnerability Target:** Raw user input supplied in medicine search, batch numbers, or sort filters injected into raw database queries.
- **Test Protocol:** Inject SQL fuzzing payloads (`' OR 1=1; --`, `UNION SELECT ...`) into all API query params and form bodies.
- **Pass Criteria:** All queries execute via SQLAlchemy 2.0 parameterized statements; zero database syntax errors or leaked schemas.

### 2.3 Malicious File Upload and Path Traversal
- **Vulnerability Target:** Uploading executable scripts disguised as CSVs (`payload.csv.py`, `../../etc/passwd`), or CSV bombs (`=cmd|' /C calc'!A0`).
- **Test Protocol:** Ingestion endpoint tested with non-CSV MIME types, disguised binaries, oversized files (> 50 MB), and formula-injected CSV cells.
- **Pass Criteria:** Ingestion pipeline verifies file extension, MIME type, and parses cells via strict non-evaluating Pydantic parsers; rejects non-compliant files immediately.

### 2.4 Brute Force and Denial of Service (DoS)
- **Vulnerability Target:** Automated credential stuffing against `/api/v1/auth/login`.
- **Test Protocol:** High-frequency script attempts 50 logins within 10 seconds.
- **Pass Criteria:** FastAPI rate-limiting middleware blocks IP after 5 failed attempts with HTTP 429 Too Many Requests.

---

## 3. Automated Security Scanning Tools

| Tool | Purpose | Stage in Pipeline |
|---|---|---|
| **Bandit** | Static AST security scanner for Python | Pre-commit / CI PR check |
| **Pip-Audit / Safety** | Dependency vulnerability scanning against CVE databases | Weekly CI / Nightly build |
| **Trivy** | Docker container vulnerability and base OS scan | Pre-deployment Docker build |
| **OWASP ZAP** | Dynamic Application Security Testing against staging API | Pre-release QA milestone |
