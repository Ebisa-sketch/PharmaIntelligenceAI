# Data Acquisition and Sourcing Strategy

---

## 1. Overview and Acquisition Hierarchy

Access to empirical pharmaceutical supply-chain records in developing healthcare systems is frequently bounded by bureaucratic data-sharing protocols, institutional governance reviews, and infrastructure limitations. 

To ensure continuous project momentum without reliance on a single unconfirmed data pathway, PharmaIntelligence AI executes a structured **multi-tiered data acquisition hierarchy**:

```
┌────────────────────────────────────────────────────────┐
│               DATA ACQUISITION HIERARCHY               │
├────────────────────────────────────────────────────────┤
│ Tier 1: Published Academic Datasets & Open Repositories│
│ Tier 2: Formal Academic Research Data Requests         │
│ Tier 3: Official Public Portals (EPSS, MoH, MFR)       │
│ Tier 4: Direct Healthcare Facility Partnership / MOU   │
│ Tier 5: Parameterized Realistic Synthetic Benchmark    │
└────────────────────────────────────────────────────────┘
```

---

## 2. Tier Details and Evaluation

### Tier 1: Published Academic Datasets and Public Repositories
- **Target:** Supplementary datasets associated with peer-reviewed open-access journal publications investigating Ethiopian pharmaceutical supply chains, inventory forecasting, and LMIS evaluations (e.g., PLOS ONE, BMC Health Services Research, ScienceDirect).
- **Action:** Systematically screen Zenodo, Dryad, Figshare, and Harvard Dataverse for open CSV/Excel files documenting facility-level consumption and stockouts.
- **Criteria:** Check Creative Commons (CC-BY / CC0) licensing terms, variable presence, and temporal completeness.

### Tier 2: Formal Academic Research Data Requests
- **Target:** Authors of prominent Ethiopian health logistics studies (e.g., Tilahun et al., 2021; Weldemariam et al., 2019; Adamu et al., 2020).
- **Action:** Dispatch standardized academic data-sharing request emails detailing the non-commercial research nature of the project, data protection commitments, institutional affiliations, and planned co-authorship / acknowledgment.
- **Template:** Provide a clear Data Use Agreement (DUA) specifying strict anonymization and research-only usage.

### Tier 3: Official Ethiopian Public Portals
- **Target Portals:**
  - *EPSS Official Portal:* https://epss.gov.et/ (Procurement guidelines, tender lists, essential drug lists).
  - *Ministry of Health (MoH) Portal:* https://moh.gov.et/ (National health service indicators, annual reports).
  - *Master Facility Registry (MFR):* https://mfrpublic.moh.gov.et/developers (Geographic coordinates, woreda locations, facility tier classifications).
  - *Dagu Portal:* https://daguportal.moh.gov.et/ (Publicly available aggregate reports).

### Tier 4: Authorized Healthcare Facility Partnerships
- **Target:** University referral hospitals (e.g., Tikur Anbessa Specialized Hospital, Gondar University Hospital, Debre Berhan Referral Hospital) through formal academic collaboration.
- **Protocol:** Obtain institutional review board (IRB) exemption/approval for aggregated, de-identified stock ledger imports. Ensure zero exposure of patient-identifiable clinical records.

### Tier 5: Parameterized Synthetic Benchmark Generator
- **Role:** Immediate, unblocked development and testing sandbox.
- **Strategy:** Build a mathematically sound synthetic generator mimicking Ethiopian pharmaceutical supply patterns (EPSS lead-time distributions, compound Poisson consumption, seasonal morbidity surges, controlled anomaly injection).
- **Mandate:** All model results obtained on synthetic data MUST be explicitly labeled as synthetic in all publications, dashboards, and reports.

---

## 3. Dataset Assessment Checklist

Before approving any acquired dataset for model training, the following checklist must be completed:

```markdown
- [ ] Source organization and primary contact documented.
- [ ] License terms and publication rights verified in writing.
- [ ] Absence of Protected Health Information (PHI) verified.
- [ ] Granularity confirmed (Daily / Weekly / Monthly).
- [ ] Number of facilities (Target: >= 3) and medicines (Target: >= 10).
- [ ] Observation period span (Target: >= 24 continuous months).
- [ ] Stockout periods distinguishable from zero demand.
- [ ] Batch numbers and expiration dates present (for expiry analysis).
- [ ] Requisition dates and delivery dates present (for lead-time analysis).
```
