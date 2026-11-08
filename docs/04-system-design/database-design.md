# Relational Database Design Specification

---

## 1. Design Overview and Principles

The PharmaIntelligence AI database is designed on **PostgreSQL 15+** adhering to Third Normal Form (3NF) principles for transactional consistency, with selective denormalization for analytical performance where appropriate.

### Key Data Tenets:
1. **Source Data Immutability:** Imported inventory records (`inventory_transactions`) are strictly append-only. Modifying an erroneous record requires posting an offsetting adjustment transaction with full audit metadata.
2. **Separation of Concerns:** Operational entities (medicines, batches, facilities) are strictly decoupled from analytical outputs (`forecasts`, `stockout_predictions`, `redistribution_recommendations`).
3. **Auditability:** Every mutable entity includes `created_at`, `updated_at`, and `created_by_user_id` fields, coupled with a central `audit_logs` table.

---

## 2. Table Specifications and Data Schema

### 2.1 Core Authentication & Access Control

#### `users`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Unique user identifier |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL | User login email |
| `username` | VARCHAR(100) | UNIQUE, NOT NULL | User handle |
| `hashed_password` | VARCHAR(255) | NOT NULL | Argon2id/Bcrypt hash |
| `full_name` | VARCHAR(150) | NOT NULL | User's full name |
| `role` | VARCHAR(50) | NOT NULL | System role (`ADMIN`, `PHARMACY_MANAGER`, etc.) |
| `assigned_facility_id` | UUID | REFERENCES facilities(id), NULLABLE | Scoped facility (for managers) |
| `assigned_region_id` | VARCHAR(100) | NULLABLE | Scoped administrative region |
| `is_active` | BOOLEAN | DEFAULT TRUE | Account active flag |
| `created_at` | TIMESTAMPTZ | DEFAULT CURRENT_TIMESTAMP | Creation timestamp |
| `updated_at` | TIMESTAMPTZ | DEFAULT CURRENT_TIMESTAMP | Last update timestamp |

---

### 2.2 Master Reference Entities

#### `facilities`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PRIMARY KEY | Unique facility ID |
| `facility_code` | VARCHAR(50) | UNIQUE, NOT NULL | National facility registry code |
| `name` | VARCHAR(255) | NOT NULL | Facility display name |
| `facility_type` | VARCHAR(50) | NOT NULL | `REFERRAL_HOSPITAL`, `PRIMARY_HOSPITAL`, `HEALTH_CENTER` |
| `region` | VARCHAR(100) | NOT NULL | Regional state (e.g., Amhara, Oromia) |
| `zone` | VARCHAR(100) | NOT NULL | Administrative zone |
| `woreda` | VARCHAR(100) | NOT NULL | Woreda district |
| `latitude` | NUMERIC(9,6) | NULLABLE | Geographic latitude |
| `longitude` | NUMERIC(9,6) | NULLABLE | Geographic longitude |
| `storage_capacity_m3` | NUMERIC(10,2) | NULLABLE | Ambient warehouse capacity |
| `has_cold_chain` | BOOLEAN | DEFAULT FALSE | Cold-chain storage availability |
| `is_active` | BOOLEAN | DEFAULT TRUE | Operational status |

#### `medicines`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PRIMARY KEY | Unique medicine ID |
| `medicine_code` | VARCHAR(50) | UNIQUE, NOT NULL | National essential medicine code |
| `generic_name` | VARCHAR(255) | NOT NULL | Generic international nonproprietary name |
| `dosage_form` | VARCHAR(100) | NOT NULL | Tablet, Capsule, Syrup, Injectable, etc. |
| `strength` | VARCHAR(100) | NOT NULL | e.g., 500mg, 1g, 250mg/5ml |
| `therapeutic_category` | VARCHAR(150) | NOT NULL | Antibiotic, Antimalarial, Antidiabetic, etc. |
| `dispensing_unit` | VARCHAR(50) | NOT NULL | Box, Strip, Bottle, Vial |
| `unit_cost_etb` | NUMERIC(12,2) | NULLABLE | Standard procurement cost in ETB |
| `requires_cold_chain` | BOOLEAN | DEFAULT FALSE | Temperature constraint (2–8°C) |
| `min_stock_days` | INTEGER | DEFAULT 30 | Standard safety buffer in days |
| `max_stock_days` | INTEGER | DEFAULT 120 | Maximum holding threshold in days |

---

### 2.3 Inventory & Batch Management

#### `medicine_batches`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PRIMARY KEY | Unique batch record ID |
| `batch_number` | VARCHAR(100) | NOT NULL | Manufacturer batch/lot number |
| `medicine_id` | UUID | REFERENCES medicines(id), NOT NULL | Associated medicine |
| `facility_id` | UUID | REFERENCES facilities(id), NOT NULL | Current holding facility |
| `manufacture_date` | DATE | NULLABLE | Production date |
| `expiry_date` | DATE | NOT NULL | Expiry date |
| `initial_quantity` | NUMERIC(12,2) | NOT NULL | Inward received quantity |
| `current_quantity` | NUMERIC(12,2) | NOT NULL | Current usable balance |
| `reserved_quantity` | NUMERIC(12,2) | DEFAULT 0.0 | Stock held for pending transfers |
| `status` | VARCHAR(50) | DEFAULT 'ACTIVE' | `ACTIVE`, `QUARANTINED`, `EXPIRED`, `DEPLETED` |
| `created_at` | TIMESTAMPTZ | DEFAULT CURRENT_TIMESTAMP | Timestamp |

#### `inventory_transactions`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PRIMARY KEY | Unique transaction record |
| `facility_id` | UUID | REFERENCES facilities(id), NOT NULL | Transacting facility |
| `medicine_id` | UUID | REFERENCES medicines(id), NOT NULL | Transacted medicine |
| `batch_id` | UUID | REFERENCES medicine_batches(id), NULLABLE | Specific batch if known |
| `transaction_type` | VARCHAR(50) | NOT NULL | `RECEIPT`, `ISSUE`, `POSITIVE_ADJUSTMENT`, `NEGATIVE_ADJUSTMENT`, `TRANSFER_IN`, `TRANSFER_OUT` |
| `quantity` | NUMERIC(12,2) | NOT NULL | Quantity transferred (positive number) |
| `transaction_date` | DATE | NOT NULL | Transaction posting date |
| `reference_doc` | VARCHAR(100) | NULLABLE | Bin-card number, RRF voucher, invoice ID |
| `import_id` | UUID | REFERENCES data_imports(id), NULLABLE | Originating batch import reference |
| `created_at` | TIMESTAMPTZ | DEFAULT CURRENT_TIMESTAMP | Ledger entry timestamp |

---

### 2.4 Data Quality & Ingestion

#### `data_imports`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PRIMARY KEY | Unique import record |
| `facility_id` | UUID | REFERENCES facilities(id), NOT NULL | Target facility |
| `uploaded_by_user_id` | UUID | REFERENCES users(id), NOT NULL | Ingesting user |
| `filename` | VARCHAR(255) | NOT NULL | Original upload filename |
| `file_hash_sha256` | VARCHAR(64) | NOT NULL | Integrity and deduplication hash |
| `total_rows` | INTEGER | NOT NULL | Total rows in file |
| `valid_rows` | INTEGER | NOT NULL | Accepted transaction rows |
| `rejected_rows` | INTEGER | NOT NULL | Discarded error rows |
| `dq_score` | NUMERIC(5,2) | NOT NULL | Computed Quality Score (0–100%) |
| `created_at` | TIMESTAMPTZ | DEFAULT CURRENT_TIMESTAMP | Ingestion timestamp |

#### `data_quality_issues`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PRIMARY KEY | Unique issue identifier |
| `import_id` | UUID | REFERENCES data_imports(id), NOT NULL | Ingestion run reference |
| `facility_id` | UUID | REFERENCES facilities(id), NOT NULL | Affected facility |
| `medicine_id` | UUID | REFERENCES medicines(id), NULLABLE | Affected medicine if identifiable |
| `issue_type` | VARCHAR(100) | NOT NULL | `RECONCILIATION_ERROR`, `NEGATIVE_STOCK`, `ANOMALOUS_SPIKE`, `INVALID_DATE` |
| `severity` | VARCHAR(20) | NOT NULL | `CRITICAL`, `WARNING`, `INFO` |
| `details` | JSONB | NOT NULL | Raw row data and mathematical discrepancy details |
| `created_at` | TIMESTAMPTZ | DEFAULT CURRENT_TIMESTAMP | Flagging timestamp |

---

### 2.5 Predictions, Recommendations & Governance

#### `demand_forecasts`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PRIMARY KEY | Unique forecast record |
| `facility_id` | UUID | REFERENCES facilities(id), NOT NULL | Facility |
| `medicine_id` | UUID | REFERENCES medicines(id), NOT NULL | Medicine |
| `forecast_horizon` | VARCHAR(20) | NOT NULL | e.g., `2026-12` (Month horizon) |
| `predicted_demand` | NUMERIC(12,2) | NOT NULL | Mean predicted consumption |
| `p10_lower_bound` | NUMERIC(12,2) | NULLABLE | 10th percentile bound |
| `p90_upper_bound` | NUMERIC(12,2) | NULLABLE | 90th percentile bound |
| `model_name` | VARCHAR(100) | NOT NULL | Model identifier (e.g., `LightGBM-v1.2`) |
| `is_decensored` | BOOLEAN | DEFAULT TRUE | Stockout de-censoring applied flag |
| `created_at` | TIMESTAMPTZ | DEFAULT CURRENT_TIMESTAMP | Computation timestamp |

#### `redistribution_recommendations`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PRIMARY KEY | Unique recommendation ID |
| `donor_facility_id` | UUID | REFERENCES facilities(id), NOT NULL | Sourcing facility |
| `recipient_facility_id` | UUID | REFERENCES facilities(id), NOT NULL | Target shortage facility |
| `medicine_id` | UUID | REFERENCES medicines(id), NOT NULL | Medicine to transfer |
| `batch_id` | UUID | REFERENCES medicine_batches(id), NOT NULL | Selected batch |
| `recommended_quantity` | NUMERIC(12,2) | NOT NULL | Transfer quantity |
| `distance_km` | NUMERIC(8,2) | NOT NULL | Estimated transit distance |
| `status` | VARCHAR(50) | DEFAULT 'PROPOSED' | `PROPOSED`, `ACCEPTED`, `REJECTED`, `DISPATCHED`, `COMPLETED` |
| `rejection_reason` | TEXT | NULLABLE | Justification if rejected by user |
| `reviewed_by_user_id` | UUID | REFERENCES users(id), NULLABLE | Approving/rejecting user |
| `reviewed_at` | TIMESTAMPTZ | NULLABLE | Action timestamp |
| `created_at` | TIMESTAMPTZ | DEFAULT CURRENT_TIMESTAMP | Recommendation generation timestamp |

#### `audit_logs`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PRIMARY KEY | Unique audit ID |
| `user_id` | UUID | REFERENCES users(id), NULLABLE | Actor user |
| `action` | VARCHAR(100) | NOT NULL | e.g., `USER_LOGIN`, `TRANSFER_APPROVE`, `FILE_UPLOAD` |
| `resource_type` | VARCHAR(100) | NOT NULL | e.g., `redistribution_recommendations` |
| `resource_id` | UUID | NULLABLE | ID of target entity |
| `ip_address` | VARCHAR(45) | NULLABLE | Client IP address |
| `changes` | JSONB | NULLABLE | Old vs new state delta |
| `created_at` | TIMESTAMPTZ | DEFAULT CURRENT_TIMESTAMP | Event timestamp |
