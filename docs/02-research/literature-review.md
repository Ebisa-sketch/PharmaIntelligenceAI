# Literature Review: Artificial Intelligence and Optimization in Pharmaceutical Supply Chains

---

## 1. Introduction

Pharmaceutical supply chains differ fundamentally from commercial retail logistics due to the critical nature of commodities, strict regulatory mandates, temperature and storage constraints, finite batch shelf-lives, and the severe clinical consequences of stockouts. In low- and middle-income countries (LMICs), particularly across Sub-Saharan Africa and Ethiopia, these complexities are compounded by infrastructure deficits, volatile funding, fragmented data architectures, and prolonged supply lead times.

This literature review synthesizes prior research across five key themes:
1. Pharmaceutical inventory management challenges in LMICs and Ethiopia.
2. Time-series and intermittent demand forecasting for essential medicines.
3. Machine learning approaches to stockout and inventory risk classification.
4. Batch-level expiry modeling and perishable inventory theory.
5. Lateral inventory transshipment and mathematical redistribution optimization.
6. Explainable Artificial Intelligence (XAI) in clinical and operational decision-support systems.

---

## 2. Pharmaceutical Supply Chain Realities in Ethiopia

Public health logistics in Ethiopia operates through a multi-tiered public health system coordinated by the **Ethiopian Pharmaceuticals Supply Service (EPSS)** (formerly PFSA). EPSS oversees central and regional distribution hubs that supply federal referral hospitals, regional hospitals, primary hospitals, and health centers.

Extensive empirical studies have documented persistent supply-chain vulnerabilities in this environment:
- **Tilahun et al. (2021)** and **Shewarega et al. (2015)** highlighted that public health facilities frequently experience stockouts of life-saving medicines (e.g., maternal oxytocics, artemisinin-based combination therapies, and oral antibiotics), with stockout durations often exceeding 30–60 consecutive days per year.
- **Weldemariam et al. (2019)** evaluated medicine wastage across public health facilities, revealing that millions of Ethiopian Birr worth of essential pharmaceuticals expire on facility shelves annually due to poor quantification, irrational requisitioning, pushing of short-dated medicines by central depots, and inadequate inter-facility communication.
- **Adamu et al. (2020)** surveyed the adoption of the Dagu eLMIS, concluding that while Dagu digitizes inventory transactions, its effectiveness is hindered by incomplete bin card reconciliation, erratic power and network connectivity, and the absence of forward-looking predictive analytics.

---

## 3. Medicine Demand Forecasting and the Censoring Dilemma

### 3.1 Intermittent and Lumpy Demand Modeling
Traditional time-series models (such as ARIMA and Exponential Smoothing) assume continuous, normally distributed demand. However, pharmaceutical consumption in district hospitals and rural health centers often exhibits intermittent or lumpy characteristics, marked by extended periods of zero consumption interspersed with sporadic, variable spikes.
- **Croston (1972)** established the foundational approach for intermittent demand by decomposing time series into two independent components: the non-zero demand size and the inter-arrival interval between demands.
- **Syntetos and Boylan (2005)** identified a positive bias in Croston’s estimator and proposed the **Syntetos-Boylan Approximation (SBA)**.
- **Teunter, Syntetos, and Babai (2011)** formulated the **TSB model**, which updates demand probabilities on every period, making it substantially more responsive to demand obsolescence.

### 3.2 Machine Learning and Stockout Censoring
Recent studies demonstrate the superiority of tree-based ensemble methods (e.g., Random Forest, LightGBM, and XGBoost) in capturing non-linear consumption patterns influenced by seasonality, facility type, and clinical morbidity data.
However, a pervasive issue identified by **Lau and Lau (1996)** and expanded in healthcare by **Huh et al. (2009)** is **stockout censoring**: when inventory drops to zero, recorded consumption drops to zero regardless of true clinical demand. Treating observed historical consumption as unconstrained demand causes machine learning models to underestimate future requirements. De-censoring techniques, including Tobit regression and in-stock day normalization, are essential to avoid perpetuating supply shortages.

---

## 4. Stockout Risk Classification

While forecasting predicts expected point quantities, operational managers require risk-based classification to prioritize scarce attention.
- Recent literature leverages supervised classification (Logistic Regression, Gradient Boosted Decision Trees) to predict binary stockout occurrences over specific planning horizons (e.g., 30, 60, 90 days).
- Key predictive features highlighted across studies include: current Days of Stock Remaining (DSR), lead time variance of recent replenishment cycles, safety stock coverage ratios, and supplier order status.
- Researchers emphasize the necessity of **calibrated probability estimates** (e.g., Platt scaling or isotonic regression) rather than uncalibrated classification scores, ensuring that a predicted 70% risk corresponds to an empirical 70% failure rate.

---

## 5. Perishable Inventory Control and Expiry Prevention

The theoretical foundation for managing expiring inventory originates from perishable inventory theory (**Nahmias, 1982**; **Goyal and Giri, 2001**).
In healthcare, issuing policies strictly follow the **First-Expired-First-Out (FEFO)** rule. However, deterministic shelf-life tracking alone is insufficient when consumption fluctuates.
- Coupling FEFO depletion queues with stochastic demand forecasts enables the calculation of **Projected Unused Stock at Expiry (PUSE)**.
- Identifying PUSE months in advance transforms expiry management from passive post-mortem write-offs into proactive redistribution opportunities.

---

## 6. Lateral Transshipment and Redistribution Optimization

Lateral transshipment—the transfer of inventory between facilities at the same echelon of a supply chain—has been extensively studied in commercial spare-parts logistics (**Paterson et al., 2011**).
In healthcare, lateral transshipment offers a high-impact, low-capital strategy to correct geographic supply-demand imbalances:
- **Mixed-Integer Linear Programming (MILP)** models allow system-wide optimization to minimize total shortage penalties, transfer costs, and expiry risks simultaneously.
- Essential constraints in humanitarian and public health contexts include:
  1. *Donor preservation:* Ensuring donor clinics retain a minimum safety threshold to prevent "robbing Peter to pay Paul".
  2. *Shelf-life validation:* Guaranteeing transferred batches possess sufficient residual life to be absorbed by the recipient.
  3. *Feasibility bounds:* Respecting geographic travel distance and maximum payload limits.

---

## 7. Explainable Artificial Intelligence (XAI) in Decision Support

Implementing AI in healthcare operations encounters steep adoption barriers if recommendations appear opaque.
- **Lundberg and Lee (2017)** introduced **SHAP (SHapley Additive exPlanations)**, providing mathematically sound, game-theoretic local feature attributions.
- In supply chain contexts, XAI allows pharmacy managers to see *why* an alert was generated (e.g., *"Stockout risk is 82% primarily due to a 45-day delay in EPSS delivery order #104 and a 30% surge in pediatric malaria cases"*). Transparent explanations foster clinical confidence and enable swift verification.

---

## 8. Summary of Literature Insights

The literature strongly supports an integrated approach combining data validation, de-censored forecasting, dual-risk estimation (stockout + expiry), constrained MILP optimization, and explainable decision-support interfaces. The subsequent document examines existing systems to contextualize how PharmaIntelligence AI addresses the specific technological gaps identified in this review.
