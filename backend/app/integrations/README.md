# External Integrations Architecture

This directory is designed for data adapters, logistics systems, and external health record connectors.

## Ethiopian Health System Context
- **Dagu (Electronic Logistics Management Information System)**: Adapters for Dagu export formats (CSV/Excel) and future API endpoints.
- **ForLab+**: Laboratory and diagnostics forecasting logistics data adapter.
- **DHIS2**: Aggregate health indicators and facility master list synchronization.
- **Standard Logistics Formats**: Electronic stock card imports, standard batch tracing manifests, and distribution requisition sheets.

## Architecture
Integrations follow an adapter pattern with strict validation, schema normalization, and idempotency guarantees before raw data enters the staging and production databases.
