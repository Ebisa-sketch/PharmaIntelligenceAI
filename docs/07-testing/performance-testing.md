# Performance, Stress, and Scalability Testing

---

## 1. Objectives and Benchmarking Scope

PharmaIntelligence AI must perform reliably across varied infrastructure conditions, ranging from low-spec dual-core desktop computers in rural Ethiopian health centers to multi-node deployments serving regional health bureaus.

Performance testing evaluates three primary workloads:
1. **Interactive API & Dashboard Response Times:** UI responsiveness under concurrent user browsing.
2. **Bulk Ingestion Throughput:** Processing speed and memory consumption during multi-thousand-row CSV imports.
3. **Mathematical Solver Scalability:** CPU and RAM utilization when running MILP redistribution optimization over increasing network sizes.

---

## 2. Key Performance Indicators (KPIs)

| Workload Metric | Target Benchmark | Maximum Tolerable Limit |
|---|---|---|
| **API Response (P95)** | $< 350\text{ ms}$ | $< 1,000\text{ ms}$ |
| **API Response (P99)** | $< 600\text{ ms}$ | $< 2,000\text{ ms}$ |
| **10,000-Row CSV Ingestion** | $< 10\text{ seconds}$ | $< 25\text{ seconds}$ |
| **MILP Optimization (10 Facilities, 20 Medicines)** | $< 3\text{ seconds}$ | $< 10\text{ seconds}$ |
| **Concurrent Users (Single Instance, 4GB RAM)**| 50 active users | — |
| **Database Connection Pool Exhaustion** | 0 connection drops under peak load | — |

---

## 3. Performance Testing Methodologies

### 3.1 Load & Stress Testing (Locust)
- **Tool:** Locust (Python-based distributed load testing).
- **Test Profile:**
  - 50 concurrent simulated users executing realistic user journeys (browsing dashboards, checking inventory, filtering batches, requesting forecasts).
  - Ramp-up: 5 users added per second until reaching peak load, held for 15 minutes.
  - Metrics captured: Requests per second (RPS), error rate, latency percentiles ($P_{50}, P_{90}, P_{95}, P_{99}$).

### 3.2 Ingestion Benchmark Test
- **Tool:** Pytest benchmark suite with varying file sizes:
  - 1,000 rows (Small facility monthly extract).
  - 10,000 rows (Medium hospital multi-month extract).
  - 100,000 rows (Regional historical consolidation).
- **Monitoring:** Track peak memory (RAM) using `tracemalloc` to prevent out-of-memory (OOM) crashes in constrained hardware environments.

### 3.3 Solver Scalability Benchmark
- Evaluate Google OR-Tools solver execution time as facility network size scales:
  - Small Cluster: 3 facilities, 5 medicines ($\approx 15$ variables).
  - Medium Cluster: 10 facilities, 25 medicines ($\approx 2,500$ variables).
  - Large Regional Network: 30 facilities, 50 medicines ($\approx 45,000$ variables).
- **Timeout Policy:** Solver hard timeout configured at 10.0 seconds. If an exact optimal integer solution is not proven within 10 seconds, the solver returns the best feasible solution with a logged optimality gap metric.
