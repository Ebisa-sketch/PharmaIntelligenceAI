# PharmaIntelligence AI - Data Sources Catalog

This catalog outlines all primary, secondary, and external data sources integrated into the platform.

| Source ID | Source Name | Description | Ingestion Frequency | Format | Target Storage |
|:----------|:------------|:------------|:--------------------|:-------|:---------------|
| `SRC-ERP-01` | Pharmacy ERP Sales | Daily point-of-sale dispensing and prescription fills | Hourly Batch / CDC | Parquet / PostgreSQL | `data/raw/sales/` |
| `SRC-WMS-01` | Central Warehouse WMS | Stock receipt, dispatch, quarantine, and inter-branch transfers | Real-time Webhooks | JSON / PostgreSQL | `data/raw/transfers/` |
| `SRC-FDA-01` | FDA National Drug Code | Reference drug information, packaging, dosage forms | Monthly Sync | XML / CSV | `data/external/ndc/` |
| `SRC-SYN-01` | Synthetic Scenario Engine | Synthetic benchmark and epidemiological surge generator | On-Demand Script | CSV / Parquet | `data/synthetic/` |
| `SRC-SUP-01` | Distributor EDI 852/855 | Vendor inventory status and purchase order acknowledgments | Daily | EDI / JSON | `data/raw/edi/` |
| `SRC-IOT-01` | Cold-Chain IoT Telemetry | Temperature and humidity sensor feeds for sensitive stock | 5 min Stream | MQTT / TimeSeries | `data/interim/iot/` |
