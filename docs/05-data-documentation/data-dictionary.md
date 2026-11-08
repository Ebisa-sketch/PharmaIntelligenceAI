# Data Dictionary and Field Specifications

---

## 1. Overview

This data dictionary provides explicit semantic definitions, data types, validation constraints, and permissible values for all data attributes processed within the PharmaIntelligence AI data pipeline.

---

## 2. Entity Field Definitions

### 2.1 Facility Records (`facilities.csv`)

| Field Name | Data Type | Nullable | Description / Permissible Values | Example |
|---|---|---|---|---|
| `facility_code` | String (50) | No | Unique national health facility identifier | `ETH-AM-DBRH-01` |
| `name` | String (255) | No | Full official name of the health facility | `Debre Berhan Referral Hospital` |
| `facility_type` | Enum | No | `REFERRAL_HOSPITAL`, `PRIMARY_HOSPITAL`, `HEALTH_CENTER` | `REFERRAL_HOSPITAL` |
| `region` | String (100) | No | Administrative region (FDRE Regional State) | `Amhara` |
| `zone` | String (100) | No | Administrative zone | `North Shewa` |
| `woreda` | String (100) | No | Administrative district / woreda | `Debre Berhan Zuria` |
| `latitude` | Decimal (9,6) | Yes | Decimal geographic latitude (-90.0 to +90.0) | `9.679120` |
| `longitude` | Decimal (9,6) | Yes | Decimal geographic longitude (-180.0 to +180.0) | `39.532840` |
| `has_cold_chain` | Boolean | No | Indicates functional 2–8°C cold chain storage | `TRUE` |

---

### 2.2 Medicine Records (`medicines.csv`)

| Field Name | Data Type | Nullable | Description / Permissible Values | Example |
|---|---|---|---|---|
| `medicine_code` | String (50) | No | Unique essential medicine catalog identifier | `MED-AMOX-500` |
| `generic_name` | String (255) | No | International Nonproprietary Name (INN) | `Amoxicillin` |
| `dosage_form` | String (100) | No | Pharmaceutical physical formulation | `Capsule` |
| `strength` | String (100) | No | Active pharmaceutical ingredient concentration | `500mg` |
| `therapeutic_category` | String (150) | No | Primary clinical classification | `Anti-infective / Antibiotic` |
| `dispensing_unit` | String (50) | No | Standard unit of issue / count | `100 Capsules Box` |
| `unit_cost_etb` | Decimal (12,2) | Yes | Standard acquisition cost in Ethiopian Birr | `185.50` |
| `requires_cold_chain` | Boolean | No | Flag indicating mandatory refrigeration | `FALSE` |
| `min_stock_days` | Integer | No | Standard safety buffer in operational days | `30` |

---

### 2.3 Inventory Transactions (`inventory_transactions.csv`)

| Field Name | Data Type | Nullable | Description / Permissible Values | Example |
|---|---|---|---|---|
| `transaction_id` | String (100) | No | Unique identifier for transaction line | `TXN-2026-009182` |
| `facility_code` | String (50) | No | Foreign reference to `facilities.facility_code` | `ETH-AM-DBRH-01` |
| `medicine_code` | String (50) | No | Foreign reference to `medicines.medicine_code` | `MED-AMOX-500` |
| `batch_number` | String (100) | Yes | Batch/lot identifier if tracked on bin card | `B2025-08A` |
| `transaction_type` | Enum | No | `RECEIPT`, `ISSUE`, `POS_ADJUST`, `NEG_ADJUST`, `TRANSFER_IN`, `TRANSFER_OUT` | `ISSUE` |
| `quantity` | Decimal (12,2) | No | Positive transacted quantity (must be $> 0$) | `250.00` |
| `transaction_date` | Date (ISO) | No | Date of occurrence (`YYYY-MM-DD`) | `2026-10-14` |
| `reference_doc` | String (100) | Yes | Source document voucher number | `RRF-OCT-014` |

---

### 2.4 Batch Master & Expiry Records (`medicine_batches.csv`)

| Field Name | Data Type | Nullable | Description / Permissible Values | Example |
|---|---|---|---|---|
| `batch_number` | String (100) | No | Manufacturer lot code | `LOT-OX-2026` |
| `facility_code` | String (50) | No | Holding facility code | `ETH-AM-HC-04` |
| `medicine_code` | String (50) | No | Associated medicine identifier | `MED-OXY-10IU` |
| `manufacture_date` | Date (ISO) | Yes | Date of chemical manufacture | `2025-04-01` |
| `expiry_date` | Date (ISO) | No | Date of chemical expiration | `2027-03-31` |
| `current_quantity` | Decimal (12,2) | No | Unused stock physically on shelf | `1200.00` |
| `reserved_quantity` | Decimal (12,2) | No | Stock allocated for pending transfers | `300.00` |
| `batch_status` | Enum | No | `ACTIVE`, `QUARANTINED`, `EXPIRED`, `DEPLETED` | `ACTIVE` |

---

### 2.5 Replenishment & Lead-Time Records (`replenishment_orders.csv`)

| Field Name | Data Type | Nullable | Description / Permissible Values | Example |
|---|---|---|---|---|
| `order_id` | String (100) | No | Unique requisition or purchase order ID | `EPSS-ORD-9021` |
| `facility_code` | String (50) | No | Requesting facility | `ETH-AM-DBRH-01` |
| `medicine_code` | String (50) | No | Ordered commodity | `MED-MET-500` |
| `order_date` | Date (ISO) | No | Date requisition was placed | `2026-08-01` |
| `order_quantity` | Decimal (12,2) | No | Quantity requested | `5000.00` |
| `expected_date` | Date (ISO) | Yes | Estimated arrival date | `2026-08-25` |
| `delivery_date` | Date (ISO) | Yes | Actual arrival date (null if pending) | `2026-09-04` |
| `received_quantity` | Decimal (12,2) | Yes | Quantity delivered (null if pending) | `4800.00` |
| `order_status` | Enum | No | `PENDING`, `PARTIALLY_DELIVERED`, `COMPLETED`, `CANCELLED` | `COMPLETED` |
