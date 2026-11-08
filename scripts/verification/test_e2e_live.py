"""
PharmaIntelligence AI - Comprehensive Live End-to-End System Verification Script

Tests the integration of:
1. Database (SQLite/PostgreSQL connectivity & seeded data)
2. FastAPI Backend API & OAuth2/JSON authentication
3. Data Engineering (Ingestion preview & 5D DQI Engine)
4. AI Demand Forecasting (Syntetos-Boylan, Croston-SBA, HistGradientBoosting)
5. Stockout Risk Intelligence with TreeSHAP explainability
6. FEFO Batch Expiration Simulation
7. Google OR-Tools SCIP MILP Lateral Redistribution Optimization
"""

import os
import sys
from datetime import date, timedelta

# Ensure backend root is on sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
BACKEND_DIR = os.path.join(PROJECT_ROOT, "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from fastapi.testclient import TestClient
from app.main import app
from app.database.connection import SessionLocal
from app.models import Facility, Medicine, Batch, Inventory, User, Role


def run_verification():
    print("=" * 70)
    print("PHARMAINTELLIGENCE AI - COMPREHENSIVE E2E SYSTEM VERIFICATION")
    print("=" * 70)

    # 1. Database Check
    print("\n[1/7] Checking Database Connection & Seed Data...")
    db = SessionLocal()
    try:
        facility_count = db.query(Facility).count()
        medicine_count = db.query(Medicine).count()
        user_count = db.query(User).count()
        batch_count = db.query(Batch).count()
        inventory_count = db.query(Inventory).count()

        print(f"  ✓ Connected to database successfully.")
        print(f"  ✓ Facilities registered: {facility_count}")
        print(f"  ✓ Essential Medicines:   {medicine_count}")
        print(f"  ✓ Active Batches:       {batch_count}")
        print(f"  ✓ Inventory records:    {inventory_count}")
        print(f"  ✓ System Users:         {user_count}")
        assert facility_count > 0, "No facilities found in database"
        assert medicine_count > 0, "No medicines found in database"
    finally:
        db.close()

    # 2. FastAPI Liveness & Readiness
    print("\n[2/7] Testing FastAPI Health Checks...")
    client = TestClient(app)
    live_res = client.get("/health")
    assert live_res.status_code == 200, f"Liveness check failed: {live_res.text}"
    ready_res = client.get("/api/v1/health")
    assert ready_res.status_code == 200, f"Readiness check failed: {ready_res.text}"
    print("  ✓ /health returned 200 OK (Liveness probe)")
    print("  ✓ /api/v1/health returned 200 OK (Readiness probe: Database & SCIP operational)")

    # 3. Authentication & RBAC
    print("\n[3/7] Testing Authentication & RBAC...")
    login_res = client.post(
        "/api/v1/auth/login/json",
        json={"email": "admin@pharmaintelligence.et", "password": "Admin123!Secure"},
    )
    assert login_res.status_code == 200, f"Login failed: {login_res.text}"
    token_data = login_res.json()
    token = token_data["token"]["access_token"]
    user = token_data["user"]
    headers = {"Authorization": f"Bearer {token}"}
    print(f"  ✓ Admin logged in: {user['full_name']} ({user['role']})")
    print(f"  ✓ Access Token generated: {token[:20]}...")

    # 4. Data Quality 5D Assessment
    print("\n[4/7] Testing Data Quality Assessment Engine (DQI)...")
    dqi_res = client.get("/api/v1/data-quality/facilities/1/assessment", headers=headers)
    assert dqi_res.status_code == 200, f"DQI assessment failed: {dqi_res.text}"
    dqi_data = dqi_res.json()
    print(f"  ✓ Facility: {dqi_data['facility_name']}")
    print(f"  ✓ Weighted DQI Score: {dqi_data['dqi_score']}% ({dqi_data['status']})")
    for dim in dqi_data["dimensions"]:
        print(f"    - {dim['dimension']}: {dim['score']}% ({dim['status']})")

    # 5. Demand Forecasting & Algorithm Benchmarking
    print("\n[5/7] Testing Demand Forecasting & Syntetos-Boylan Classifier...")
    forecast_res = client.get(
        "/api/v1/forecasting/facilities/1/medicines/1?horizon_days=90&model_type=ensemble",
        headers=headers,
    )
    assert forecast_res.status_code == 200, f"Forecasting failed: {forecast_res.text}"
    f_data = forecast_res.json()
    print(f"  ✓ Generated 90-day forecast: {f_data['forecast_value']:.1f} units")
    print(f"  ✓ 95% Confidence Interval: [{f_data['confidence_interval_lower']:.1f}, {f_data['confidence_interval_upper']:.1f}]")
    print(f"  ✓ Demand Pattern: {f_data['demand_category']} (ADI={f_data['adi']:.2f}, CV2={f_data['cv2']:.2f})")

    compare_res = client.get(
        "/api/v1/forecasting/facilities/1/medicines/1/compare",
        headers=headers,
    )
    assert compare_res.status_code == 200, f"Model comparison failed: {compare_res.text}"
    c_data = compare_res.json()
    print(f"  ✓ Algorithm benchmarked: Recommended model is {c_data['recommended_model']}")
    for m_name, m_metrics in c_data["models_evaluated"].items():
        print(f"    - {m_name}: WAPE={m_metrics['wape']:.1f}%, MASE={m_metrics['mase']:.2f}")

    # 6. Stockout & Expiry Risk Intelligence
    print("\n[6/7] Testing Stockout & Expiry Risk Assessment...")
    stockout_res = client.get("/api/v1/stockout/facilities/1", headers=headers)
    assert stockout_res.status_code == 200, f"Stockout check failed: {stockout_res.text}"
    stockouts = stockout_res.json()
    print(f"  ✓ Stockout risks evaluated: {len(stockouts)} items analyzed")
    if stockouts:
        crit = stockouts[0]
        print(f"    - Item: {crit['medicine_name']} -> Risk: {crit['risk_level']} (Score={crit['stockout_risk_score']:.2f}, DSR={crit['days_until_stockout']:.1f}d)")
        print(f"    - Attributions: {[a['factor'] for a in crit.get('attributions', [])]}")

    expiry_res = client.get("/api/v1/expiry/facilities/1", headers=headers)
    assert expiry_res.status_code == 200, f"Expiry check failed: {expiry_res.text}"
    expiries = expiry_res.json()
    print(f"  ✓ FEFO Expiry risks evaluated: {len(expiries)} batches analyzed")
    if expiries:
        exp = expiries[0]
        print(f"    - Lot: {exp['batch_number']} -> PUSE: {exp['quantity_at_risk']} units at risk ({exp['estimated_loss_etb']:.2f} ETB)")

    # 7. MILP Redistribution Optimization
    print("\n[7/7] Testing SCIP MILP Redistribution Optimizer...")
    opt_res = client.post(
        "/api/v1/redistribution/optimize",
        headers=headers,
        json={
            "max_distance_km": 500.0,
            "min_expiry_months": 2,
            "cost_transport_per_km_unit": 0.02,
        },
    )
    assert opt_res.status_code == 200, f"Optimization failed: {opt_res.text}"
    proposals = opt_res.json()
    print(f"  ✓ MILP Solver executed successfully: {len(proposals)} transfer proposals found")
    if proposals:
        p = proposals[0]
        print(f"    - Proposal #{p['id']}: {p['source_facility_name']} -> {p['target_facility_name']}")
        print(f"    - Medicine: {p['medicine_name']} (Qty: {p['quantity_recommended']})")
        print(f"    - Distance: {p['transport_distance_km']:.1f} km, Logistics Cost: {p['estimated_transfer_cost_etb']:.2f} ETB")
        print(f"    - Net Value Saved: {p['prevented_wastage_cost_etb']:.2f} ETB")

    print("\n" + "=" * 70)
    print("ALL 7 SYSTEM INTEGRATION MILESTONES VERIFIED WITH ZERO ERRORS!")
    print("=" * 70)


if __name__ == "__main__":
    run_verification()
