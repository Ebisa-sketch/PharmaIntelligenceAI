# Entity-Relationship (ER) Diagram

---

## 1. Visual Entity Relationships

The following Mermaid ER diagram illustrates the relational models, cardinalities, and foreign key dependencies within PharmaIntelligence AI.

```mermaid
erDiagram
    FACILITIES ||--o{ USERS : "employs / assigns"
    FACILITIES ||--o{ MEDICINE_BATCHES : "stores"
    FACILITIES ||--o{ INVENTORY_TRANSACTIONS : "records"
    FACILITIES ||--o{ DATA_IMPORTS : "receives"
    FACILITIES ||--o{ DEMAND_FORECASTS : "has"
    FACILITIES ||--o{ REDISTRIBUTION_RECOMMENDATIONS : "donates"
    FACILITIES ||--o{ REDISTRIBUTION_RECOMMENDATIONS : "receives"

    MEDICINES ||--o{ MEDICINE_BATCHES : "categorizes"
    MEDICINES ||--o{ INVENTORY_TRANSACTIONS : "transacts"
    MEDICINES ||--o{ DEMAND_FORECASTS : "forecasted for"
    MEDICINES ||--o{ REDISTRIBUTION_RECOMMENDATIONS : "transferred in"

    MEDICINE_BATCHES ||--o{ INVENTORY_TRANSACTIONS : "allocated in"
    MEDICINE_BATCHES ||--o{ REDISTRIBUTION_RECOMMENDATIONS : "selected for"

    USERS ||--o{ DATA_IMPORTS : "uploads"
    USERS ||--o{ REDISTRIBUTION_RECOMMENDATIONS : "reviews"
    USERS ||--o{ AUDIT_LOGS : "triggers"

    DATA_IMPORTS ||--o{ DATA_QUALITY_ISSUES : "identifies"
    DATA_IMPORTS ||--o{ INVENTORY_TRANSACTIONS : "sources"

    FACILITIES {
        uuid id PK
        string facility_code
        string name
        string facility_type
        string region
        decimal latitude
        decimal longitude
        boolean has_cold_chain
    }

    MEDICINES {
        uuid id PK
        string medicine_code
        string generic_name
        string dosage_form
        string strength
        string therapeutic_category
        decimal unit_cost_etb
        boolean requires_cold_chain
    }

    MEDICINE_BATCHES {
        uuid id PK
        string batch_number
        uuid medicine_id FK
        uuid facility_id FK
        date expiry_date
        decimal current_quantity
        decimal reserved_quantity
        string status
    }

    INVENTORY_TRANSACTIONS {
        uuid id PK
        uuid facility_id FK
        uuid medicine_id FK
        uuid batch_id FK
        string transaction_type
        decimal quantity
        date transaction_date
        uuid import_id FK
    }

    DATA_IMPORTS {
        uuid id PK
        uuid facility_id FK
        uuid uploaded_by_user_id FK
        string filename
        string file_hash_sha256
        integer valid_rows
        integer rejected_rows
        decimal dq_score
    }

    DATA_QUALITY_ISSUES {
        uuid id PK
        uuid import_id FK
        uuid facility_id FK
        string issue_type
        string severity
        jsonb details
    }

    DEMAND_FORECASTS {
        uuid id PK
        uuid facility_id FK
        uuid medicine_id FK
        string forecast_horizon
        decimal predicted_demand
        decimal p10_lower_bound
        decimal p90_upper_bound
        string model_name
    }

    REDISTRIBUTION_RECOMMENDATIONS {
        uuid id PK
        uuid donor_facility_id FK
        uuid recipient_facility_id FK
        uuid medicine_id FK
        uuid batch_id FK
        decimal recommended_quantity
        decimal distance_km
        string status
        uuid reviewed_by_user_id FK
    }

    USERS {
        uuid id PK
        string email
        string username
        string role
        uuid assigned_facility_id FK
    }

    AUDIT_LOGS {
        uuid id PK
        uuid user_id FK
        string action
        string resource_type
        uuid resource_id
        jsonb changes
    }
```

---

## 2. Cardinality and Integrity Rules

1. **One-to-Many (`1:N`) Facilities to Batches:** A health facility holds zero or more inventory batches. Each batch is physically situated at exactly one facility at any given point in time.
2. **One-to-Many (`1:N`) Medicines to Batches:** A master catalog medicine record links to multiple physical batches distinguished by batch numbers and expiration dates.
3. **Many-to-One (`N:1`) Transactions to Batches:** Individual inventory transactions may link directly to a specific batch (crucial for FEFO auditability), or be recorded at the general medicine level if legacy paper records lack batch granularity.
4. **Many-to-Many (`M:N`) Facilities via Redistribution:** Lateral transfer recommendations create a directional relationship between two distinct facilities (a `donor_facility` and a `recipient_facility`). Database constraints enforce that `donor_facility_id != recipient_facility_id`.
5. **Cascading and Soft Deletion:** Critical master entities (facilities, medicines) use soft-delete flags (`is_active = FALSE`) to prevent cascading deletions of historical transaction ledgers and audit records.
