# User Roles and Role-Based Access Control (RBAC) Specification

---

## 1. Overview

PharmaIntelligence AI implements a granular **Role-Based Access Control (RBAC)** model combined with **Facility-Scope Tenancy**. This ensures that healthcare personnel only access operational records, predictive models, and administrative tools relevant to their clinical jurisdiction and legal responsibilities.

---

## 2. Defined User Roles

The system defines five primary operational roles:

```
┌────────────────────────────────────────────────────────┐
│                   ROLE HIERARCHY                       │
├──────────────────────────┬─────────────────────────────┤
│ 1. System Administrator  │ Global System Management    │
│ 2. Regional SC Officer   │ Cross-Facility Oversight    │
│ 3. Facility Manager      │ Local Store Operations      │
│ 4. Data Analyst / Res.   │ ML Experiments & Analytics  │
│ 5. Compliance Auditor    │ Read-Only Verification      │
└──────────────────────────┴─────────────────────────────┘
```

1. **System Administrator (`ROLE_ADMIN`):** Manages user accounts, assigns roles, configures facility reference data, oversees system health, and inspects security logs.
2. **Facility Pharmacy Manager (`ROLE_PHARMACY_MANAGER`):** Head pharmacist or inventory officer responsible for an individual health center or hospital. Manages local stock, uploads bin-card transaction files, reviews local expiry and stockout alerts, and approves/rejects incoming and outgoing lateral transfer requests.
3. **Regional Supply Chain Officer (`ROLE_REGIONAL_OFFICER`):** Regional Health Bureau (RHB) or EPSS Hub supply chain manager. Has multi-facility oversight across an administrative zone, initiates regional redistribution optimization runs, and mediates inter-facility transfers.
4. **Data Analyst / Researcher (`ROLE_RESEARCHER`):** Conducts data-quality profiling, runs predictive modeling experiments, tunes hyperparameters, evaluates forecasting backtests, and exports research metrics.
5. **Compliance Auditor (`ROLE_AUDITOR`):** External or internal inspector reviewing read-only audit trails, data provenance, and decision approval records for regulatory and anti-corruption oversight.

---

## 3. Permissions Matrix

| Permission Code | Description | Admin | Regional Officer | Pharmacy Manager | Researcher | Auditor |
|---|---|:---:|:---:|:---:|:---:|:---:|
| `users:manage` | Create, update, deactivate user accounts | ✅ | ❌ | ❌ | ❌ | ❌ |
| `facilities:manage` | Create or update facility master records | ✅ | ❌ | ❌ | ❌ | ❌ |
| `medicines:manage` | Manage master medicine catalog | ✅ | ❌ | ❌ | ❌ | ❌ |
| `data:import` | Upload inventory and transaction files | ✅ | ✅ | ✅ (Own Facility) | ✅ (Sandbox) | ❌ |
| `data:quality_view` | View data quality scores and issues | ✅ | ✅ | ✅ (Own Facility) | ✅ | ✅ |
| `inventory:view` | Inspect stock balances and batches | ✅ | ✅ (Region) | ✅ (Own Facility) | ✅ (Aggregated) | ✅ |
| `forecast:run` | Execute demand forecasting runs | ✅ | ✅ | ✅ (Own Facility) | ✅ | ❌ |
| `forecast:view` | View forecast outputs & uncertainty | ✅ | ✅ | ✅ | ✅ | ✅ |
| `risk:view` | View stockout and expiry risk scores | ✅ | ✅ | ✅ | ✅ | ✅ |
| `redistribute:run` | Execute redistribution optimization | ✅ | ✅ | ❌ | ✅ (Simulated) | ❌ |
| `redistribute:approve` | Accept/Reject transfer recommendation | ❌ | ✅ (Regional) | ✅ (Facility Transfer) | ❌ | ❌ |
| `audit:view` | View security and operational audit logs | ✅ | ❌ | ❌ | ❌ | ✅ |
| `models:manage` | Train, tune, and register ML models | ✅ | ❌ | ❌ | ✅ | ❌ |

---

## 4. Facility Scoping and Multi-Tenancy Rules

In addition to role permissions, database queries enforce **Facility Scoping**:
- **Scoped by Facility (`assigned_facility_id`):** `ROLE_PHARMACY_MANAGER` is restricted to records where `facility_id == current_user.assigned_facility_id`. Attempts to query another facility return HTTP `403 Forbidden`.
- **Scoped by Region (`assigned_region_id`):** `ROLE_REGIONAL_OFFICER` has access to all facilities where `facility.region_id == current_user.assigned_region_id`.
- **Unrestricted Scope:** `ROLE_ADMIN`, `ROLE_AUDITOR`, and `ROLE_RESEARCHER` (researchers operate on anonymized/synthetic or globally authorized datasets).

---

## 5. Session and Security Policies
- Inactive user sessions expire after **30 minutes** of inactivity.
- Five consecutive failed login attempts result in temporary account lockout for **15 minutes**.
- Multi-factor authentication (MFA via TOTP) is supported and recommended for administrative and regional officer roles.
