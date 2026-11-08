# PharmaIntelligence AI - Data Management

This directory structures the data pipeline for the PharmaIntelligence AI platform, managing data across ingestion stages from raw ingestion to model-ready features.

## Directory Structure

```
data/
├── raw/                 # Immutable source datasets, incoming feeds, CSVs/Parquet
├── interim/             # Cleaned and normalized intermediate representations
├── processed/           # Feature-engineered and curated datasets ready for ML/DB ingestion
├── synthetic/           # Synthetic dataset generator scripts, scenarios, and mock data
│   ├── generators/      # Generation rules and distributions
│   ├── scenarios/       # Specific stress-test and pandemic/supply-shock scenarios
│   └── sample_data/     # Pre-generated deterministic sample batches
├── external/            # External reference data (regulatory lists, NDC/RxNorm mappings)
├── schemas/             # JSON schemas defining data validation contracts
└── metadata/            # Data dictionaries, lineage, versions, and source catalogs
```

## Data Validation and Governance

- All datasets entering `processed/` must conform to the JSON schemas defined in `schemas/`.
- No sensitive patient identifiable information (PII) or unmasked internal operational credentials may be committed or stored here.
- Automated validation scripts can be executed via `scripts/data/validate_dataset.py`.
