# UI/UX Design System and Screen Architecture

---

## 1. Design System Foundations

PharmaIntelligence AI serves healthcare professionals, pharmacy technicians, and supply chain managers working under high-stress, time-sensitive conditions. The user interface adheres to human-centered design principles prioritizing **clarity, low cognitive friction, explicit transparency, and accessibility**.

### 1.1 Color Palette & Visual Semantics
To ensure accessibility for color-blind users and high visibility on low-contrast clinic monitors, all color cues are paired with distinct text tags and iconography.

| Semantic Role | Color Code (Hex) | Accessible Contrast Ratio | Visual Pairing Indicator |
|---|---|---|---|
| **Critical Risk** | Crimson Red (`#DC2626`) | > 4.5:1 against white | `[!] Alert Triangle` + Text: "CRITICAL" |
| **Warning / Moderate** | Amber Orange (`#D97706`) | > 4.5:1 against white | `[~] Alert Circle` + Text: "WARNING" |
| **Safe / Optimal** | Forest Green (`#16A34A`) | > 4.5:1 against white | `[✓] Checkmark Circle` + Text: "SAFE" |
| **Informational** | Slate Blue (`#2563EB`) | > 4.5:1 against white | `[i] Info Icon` + Text: "INFO" |
| **Surface Background**| Neutral Gray (`#F8FAFC`) | Clean, non-glare surface | — |
| **Card Surface** | Pure White (`#FFFFFF`) | Elevated with subtle border | — |

---

## 2. Global Navigation and Layout Structure

The layout utilizes a persistent responsive sidebar and a contextual header:

```
┌──────────────┬────────────────────────────────────────────────────────┐
│ PharmaIntel  │ Facility: [Debre Berhan Ref Hosp v]  User: [Dr. Abebe] │
├──────────────┼────────────────────────────────────────────────────────┤
│ 📊 Dashboard │  SYSTEM HEALTH: Operational | DATA QUALITY: 94.2% (Good)│
│ 📦 Inventory │ ┌──────────────┬──────────────┬──────────────┬─────────┐│
│ 🔍 Data Qual │ │ Stockouts    │ Expiring     │ Transfers    │ Pending ││
│ 📈 Forecasts │ │ 3 Critical   │ 2 Batches    │ 4 Feasible   │ Approvals││
│ ⚠️ Risks     │ └──────────────┴──────────────┴──────────────┴─────────┘│
│ 🔄 Transfers │                                                         │
│ 🔬 AI Lab    │ [Main Content Area: Interactive Visualizations & Tables]│
│ ⚙️ Admin     │                                                         │
└──────────────┴────────────────────────────────────────────────────────┘
```

---

## 3. Detailed Screen Architecture

### 3.1 Executive Dashboard (`/dashboard`)
- **Key Metric KPI Cards:**
  - *Imminent Stockouts:* Number of essential medicines with < 14 Days of Stock Remaining.
  - *Expiring Batch Volume:* Total units and financial value (ETB) projected to expire unused within 90 days.
  - *System Data Quality Index (DQCI):* Overall completeness score across ingested facility records.
  - *Pending Lateral Transfers:* Sourced recommendations awaiting pharmacist sign-off.
- **Top Priority Attention List:** Tabbed table allowing immediate triage of high-risk items.

### 3.2 Data Quality Center (`/data-quality`)
- **Drag-and-Drop Ingestion Dropzone:** Supports CSV, TSV, and Excel files with instant client-side format checks.
- **Import History Table:** Displays historical uploads, row counts, user provenance, and validation status.
- **Reconciliation Discrepancy Drawer:** Clicking a flagged upload opens a detailed side drawer displaying exact transaction rows where $\text{Closing} \neq \text{Opening} + \text{In} - \text{Out} \pm \text{Adj}$.

### 3.3 Forecasting Center (`/forecasting`)
- **Selector Toolbar:** Filter by Facility, Therapeutic Category, and Specific Medicine.
- **Interactive Time-Series Canvas:**
  - Historical monthly/weekly consumption points.
  - Stockout-censored periods highlighted in gray shading.
  - De-censored historical baseline comparison.
  - Forward-looking multi-horizon forecast line with shaded 80% and 95% confidence bands.
- **Model Comparison Table:** Toggle between LightGBM, Croston, TSB, and Naive baselines to inspect comparative MASE and WAPE metrics.

### 3.4 Stockout & Expiry Risk Centers (`/risks`)
- **Dual Perspective Toggle:**
  - *Stockout View:* Visualizes Days of Stock Remaining (DSR) against replenishment lead-time curves.
  - *Expiry View (FEFO Timeline):* Displays a Gantt-style shelf-life bar chart for all batches, highlighting the exact crossover point where projected consumption fails to exhaust a batch prior to expiration.

### 3.5 Lateral Redistribution Center (`/redistribution`)
- **Interactive Regional Map & Transfer Graph:** Visualizes donor facilities (green nodes) connected via directional transfer arcs to recipient facilities (red nodes).
- **Recommendation Review Card:**
  - Donor facility, Recipient facility, Medicine, Batch ID.
  - Transfer quantity and percentage of donor surplus utilized.
  - Assurance check: Confirms donor retains minimum 30-day safety buffer post-transfer.
  - Estimated road transit distance and cold-chain compliance badge.
  - Action buttons: **[Approve Transfer]**, **[Adjust Quantity]**, **[Reject Proposal]**.

### 3.6 AI Explainability Side-Drawer
- Opens upon clicking "Why this prediction?" on any risk card or forecast.
- **Waterfall / Horizontal Bar Chart:** Shows individual feature attributions (TreeSHAP values).
- **Plain-Language Summary:** Clear natural-language synthesis generated from the model features, explaining the clinical and logistical rationale.
