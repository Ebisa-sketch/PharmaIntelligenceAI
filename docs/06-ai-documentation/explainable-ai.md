# Explainable AI (XAI) and Decision Transparency

---

## 1. Rationale for Explainability in Clinical Supply Chains

In healthcare operations, algorithmic opacity ("black box" AI) creates critical friction:
- **Clinical and Legal Accountability:** Pharmacy managers bear personal regulatory responsibility for stock availability and patient safety. They will not execute recommendations they cannot verify.
- **Verification of Spurious Correlations:** In low-resource settings, noisy data can trick models into learning false patterns (e.g., associating high malaria medicine issues with rainy season floods, even if a clinic was actually closed for renovations).
- **User Trust and Adoption:** Transparent explanations build trust, converting skeptics into active collaborators who understand *why* the model made a specific prediction.

---

## 2. Technical Explainability Framework

PharmaIntelligence AI integrates a multi-layered explainability architecture:

```
┌────────────────────────────────────────────────────────┐
│                   EXPLAINABILITY LAYERS                │
├──────────────────────────┬─────────────────────────────┤
│ 1. Local TreeSHAP        │ Feature Attribution Values  │
│ 2. Transparent Rules     │ Mathematical Formulas & DSR │
│ 3. Uncertainty Bands     │ Prediction Intervals (P10/90│
│ 4. Plain-Language NLG    │ Human-Readable Summaries    │
└──────────────────────────┴─────────────────────────────┘
```

---

## 3. Local Feature Attribution via TreeSHAP

For tree-based ensemble models (LightGBM and XGBoost), the system computes exact local Shapley values using **TreeSHAP** (Lundberg et al., 2020).

### 3.1 Mathematical Foundation
For a model prediction $f(\mathbf{x})$, the Shapley attribution $\phi_i$ decomposes the prediction relative to the expected base value $\mathbb{E}[f(X)]$:
$$f(\mathbf{x}) = \phi_0 + \sum_{i=1}^M \phi_i(x)$$
where $\phi_0 = \mathbb{E}[f(X)]$ and $\phi_i(x)$ represents the marginal contribution of feature $i$ to the deviation from the average prediction.

### 3.2 Visualization in the User Interface
In the web interface, clicking "Explain Prediction" generates a Waterfall / Horizontal Bar Chart:
- **Red / Outward Bars:** Features that pushed risk upward (e.g., `+320 units due to 45-day EPSS supply delay`).
- **Blue / Inward Bars:** Features that reduced risk (e.g., `-180 units due to high safety stock reserve`).

---

## 4. Transparent Rule Attribution for Optimization

Mixed-Integer Linear Programs (MILP) are mathematically transparent by design. For every lateral transfer recommendation, the system displays the explicit binding constraints that justified the transfer:
1. **Surplus Proof:** Shows donor facility's on-hand stock vs. its local safety buffer ($S_{\text{donor}} - SS_{\text{donor}} > 0$).
2. **Deficit Proof:** Shows recipient facility's projected stockout date in the absence of transfer.
3. **Shelf-Life Proof:** Demonstrates that transferred batches will be fully absorbed at the recipient before expiration based on recipient daily consumption rate $\hat{d}_{\text{recipient}}$.
4. **Distance & Transport Proof:** Shows transit distance ($d_{ij} \le D_{\max}$) and cold-chain compatibility verification.

---

## 5. Natural Language Generation (NLG) Summaries

To ensure accessibility for non-technical pharmacy personnel, raw numerical SHAP values are translated into plain-language diagnostic summaries via parameterized templates:

#### Example Generated Diagnostic:
> *"Amoxicillin 500mg is flagged at **CRITICAL Stockout Risk (88% probability within 21 days)** at Debre Berhan Referral Hospital.  
> **Key Drivers:**  
> 1. Current usable stock (180 boxes) covers only 9 days of projected demand.  
> 2. Requisition order #4092 placed with EPSS Hub is currently delayed by 14 days past historical delivery norms.  
> 3. Seasonal pediatric respiratory illness index indicates a projected 25% demand increase this month."*
