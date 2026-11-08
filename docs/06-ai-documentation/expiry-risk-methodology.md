# Expiry Risk Intelligence and FEFO Allocation Methodology

---

## 1. Overview and Problem Context

Pharmaceutical expiration represents a total loss of public health resources. In low-resource healthcare networks, batches frequently expire not because the medicine is obsolete, but because short-dated batches were delivered to facilities with low dispensing throughput.

PharmaIntelligence AI replaces passive calendar-date warnings with a **forward-looking First-Expired-First-Out (FEFO) consumption simulation** that calculates the exact volume and monetary value of medicines at risk of expiry months in advance.

---

## 2. Mathematical Formulation: FEFO Depletion Queue

For each facility $f$ and medicine $m$, active inventory consists of $K$ distinct batches:
$$\mathcal{B}_{f,m} = \{b_1, b_2, \dots, b_K\}$$
where each batch $b_k$ is defined by:
- $Q_k$: Current usable stock quantity.
- $T_k^{\text{exp}}$: Remaining shelf life in days ($T_k^{\text{exp}} = \text{Expiry Date}_k - \text{Current Date}$).

Under national standard operating procedures, dispensing follows **First-Expired-First-Out (FEFO)**, sorting batches in ascending order of expiration:
$$T_1^{\text{exp}} \le T_2^{\text{exp}} \le \dots \le T_K^{\text{exp}}$$

---

## 3. Projected Unused Stock at Expiry (PUSE)

Let $\hat{D}_{f,m}(t)$ represent the projected daily consumption rate over time $t \ge 0$. The cumulative demand expected from today up to the expiration date $T_k^{\text{exp}}$ of batch $k$ is:
$$\hat{\mathcal{D}}_k = \sum_{t=1}^{T_k^{\text{exp}}} \hat{D}_{f,m}(t)$$

Because earlier expiring batches $b_1, \dots, b_{k-1}$ take strict dispensing precedence, the cumulative stock that must be consumed before or concurrently with batch $k$ is:
$$\mathcal{S}_k = \sum_{i=1}^k Q_i$$

### Expiry Wastage Condition:
A batch $k$ is at risk of partial or total expiry wastage if the cumulative stock $\mathcal{S}_k$ exceeds the total cumulative demand $\hat{\mathcal{D}}_k$ achievable prior to its expiration date.

The **Projected Unused Stock at Expiry (PUSE)** for batch $k$ is calculated as:
$$\text{PUSE}_k = \max\left(0, \min\left(Q_k, \mathcal{S}_k - \hat{\mathcal{D}}_k\right)\right)$$

The **Financial Value at Risk (FVR)** is:
$$\text{FVR}_k = \text{PUSE}_k \times \text{Unit Cost}_{\text{ETB}}$$

---

## 4. Stratification of Expiry Urgency

Batches are classified into three actionable operational categories:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        EXPIRY RISK CLASSIFICATION                      │
├─────────────────┬──────────────────────┬───────────────────────────────┤
│ Tier            │ Criteria             │ Operational Intervention      │
├─────────────────┼──────────────────────┼───────────────────────────────┤
│ 1. CRITICAL     │ PUSE > 0 and         │ Immediate lateral transfer    │
│    WASTE RISK   │ Remaining Life < 90d │ to high-volume facility       │
├─────────────────┼──────────────────────┼───────────────────────────────┤
│ 2. WARNING /    │ PUSE > 0 and         │ Flag for regional coordinator;│
│    SURPLUS      │ 90d <= Life < 180d   │ pause incoming replenishments │
├─────────────────┼──────────────────────┼───────────────────────────────┤
│ 3. ABSORBABLE / │ PUSE == 0            │ Normal dispensing; batch will │
│    SAFE         │                      │ be consumed prior to expiry   │
└─────────────────┴──────────────────────┴───────────────────────────────┘
```

---

## 5. Integrating Demand Uncertainty into Expiry Risk

Because demand $\hat{D}$ is stochastic, the system evaluates PUSE across the forecast distribution:
- **Optimistic Scenario ($P_{90}$ Demand):** Minimum projected waste.
- **Expected Scenario ($P_{50}$ Demand):** Baseline projected waste.
- **Conservative Scenario ($P_{10}$ Demand):** Maximum projected waste if consumption slows.

This gives decision-makers confidence intervals on potential financial losses, justifying proactive lateral transfers before medicines reach the point of total destruction.
