# Dataset Specification

---

## 1. Overview and Data Architecture

PharmaIntelligence AI relies on structured pharmaceutical supply-chain datasets capable of supporting historical demand analysis, stock reconciliation, batch-level shelf-life tracking, and multi-facility spatial network modeling.

This specification details the structural requirements, schemas, and operational constraints for both empirical secondary datasets (e.g., published Ethiopian eLMIS records) and the synthetic benchmark generator developed within this project.

---

## 2. Core Data Domains

The data model encompasses six interconnected analytical domains:

```
┌────────────────────────────────────────────────────────┐
│                   DATA DOMAIN SCHEMAS                  │
├──────────────────────────┬─────────────────────────────┤
│ 1. Facility Master       │ Geographic & Capacity Data  │
│ 2. Medicine Master       │ Formulary, Units & Limits   │
│ 3. Inventory Balances    │ Snapshots & Stock on Hand   │
│ 4. Transaction Ledgers   │ Receipts, Issues, Adjusts   │
│ 5. Batch & Expiry        │ Lot Numbers & Shelf-Life    │
│ 6. Replenishment Orders  │ Requisitions & Lead Times   │
└──────────────────────────┴─────────────────────────────┘
```

---

## 3. Dataset Characteristics and Requirements

### 3.1 Temporal Resolution and Granularity
- **Granularity:** Monthly or Weekly aggregation for high-level forecasting; Daily transaction timestamps for bin-card reconciliation and lead-time analysis.
- **Historical Horizon:** Minimum 24 months (ideally 36 months) of continuous observation to allow seasonal decomposition, train/validation/test chronological splitting, and backtesting.

### 3.2 Geographic and Institutional Scope
- **Network Hierarchy:** Tiered network including at least one Referral Hospital, 2 Primary District Hospitals, and 3–5 Health Centers located within a shared regional supply corridor (e.g., within 100 km radius) to validate redistribution models.

### 3.3 Medicine Basket Selection
The dataset MUST contain a representative basket of essential medicines reflecting diverse demand patterns (Syntetos-Boylan categories):
- *High-Volume Fast-Moving:* Amoxicillin 500mg, Paracetamol 500mg (Smooth demand).
- *Intermittent / Critical Life-Saving:* Oxytocin 10 IU/ml Injection, Magnesium Sulfate 50% Injection (Intermittent demand).
- *Chronic Disease Maintenance:* Metformin 500mg, Enalapril 5mg (Smooth to Erratic demand).
- *Seasonal Morbidity Commodities:* Artemether-Lumefantrine (Coartem) (Seasonal/Lumpy demand).

---

## 4. Synthetic Data Generation Protocol

Given that real-world healthcare records may face access delays or confidentiality barriers, the project specifies an advanced synthetic dataset generator:
1. **Demand Generation:** Generates non-negative integer consumption series using compound Poisson-gamma or Negative Binomial distributions parameterized by facility patient volume.
2. **Seasonality Injection:** Sinusoidal seasonal multipliers reflecting rainy season malaria and respiratory peaks.
3. **Stockout Censoring Simulation:** When simulated inventory reaches zero, simulated recorded consumption is truncated to zero while underlying latent demand continues.
4. **Lead-Time Modeling:** Random draws from log-normal distributions ($\mu=21\text{ days}, \sigma=10\text{ days}$) representing EPSS delivery delays.
5. **Batch Generation:** Discrete batches assigned randomized manufacture and expiry dates (shelf life between 12 and 36 months), tracking lot-specific drawdowns using FEFO priority.
6. **Controlled Anomaly Injection:** Deterministic injection of known anomalies (e.g., negative stock, missing transaction rows, mathematical reconciliation discrepancies) to rigorously benchmark the Data Quality Intelligence engine.

---

## 5. Dataset Validation and Acceptance Criteria

Before any dataset (real or synthetic) is accepted into the analytical pipeline, it must satisfy:
- Completeness of primary reference keys (Facility Code, Medicine Code).
- Less than 10% unresolvable missingness in consumption series.
- Verification that stockout intervals are explicitly distinguishable from zero-demand periods.
- Full provenance documentation regarding licensing, owner, and generation parameters.
