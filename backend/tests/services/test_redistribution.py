import pytest
from datetime import date, timedelta
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import Facility, Medicine, Inventory, Batch, RedistributionRecommendation
from app.ml.redistribution_optimizer import MILPRedistributionOptimizer, haversine_distance_km
from app.ml.simulation_scenarios import RedistributionSimulator
from app.services.redistribution_service import RedistributionService
from app.schemas.recommendation import RedistributionOptimizationRun, SimulationScenarioRequest


def get_auth_token(client: TestClient) -> str:
    res = client.post(
        "/api/v1/auth/login/json",
        json={"email": "testadmin@pharmaintelligence.et", "password": "AdminSecret123!"},
    )
    return res.json()["token"]["access_token"]


# ──────────────────────────────────────────────────────────────
# 1. Distance & Geometry Tests
# ──────────────────────────────────────────────────────────────

def test_haversine_distance():
    # Tikur Anbessa (9.0054, 38.7468) to St. Paul's (9.0400, 38.7300) in Addis Ababa
    dist = haversine_distance_km(9.0054, 38.7468, 9.0400, 38.7300)
    assert 3.5 < dist < 5.5

    # Same location -> 0 km
    assert haversine_distance_km(9.0054, 38.7468, 9.0054, 38.7468) == 0.0


# ──────────────────────────────────────────────────────────────
# 2. MILP Optimizer Tests
# ──────────────────────────────────────────────────────────────

def test_milp_redistribution_optimizer():
    optimizer = MILPRedistributionOptimizer(max_distance_km=100.0, min_shelf_life_days=60)
    today = date.today()

    facilities = [
        {"id": 1, "name": "Facility Donor", "latitude": 9.00, "longitude": 38.70},
        {"id": 2, "name": "Facility Recipient", "latitude": 9.04, "longitude": 38.73},
    ]
    medicines = [
        {"id": 1, "name": "Amoxicillin 500mg", "minimum_stock_level": 500.0}
    ]
    # Donor has 2000 units (Surplus = 1500 units above safety stock 500)
    # Recipient has 100 units (Deficit = 400 units below safety stock 500)
    inventories = [
        {"id": 1, "facility_id": 1, "medicine_id": 1, "usable_stock": 2000.0},
        {"id": 2, "facility_id": 2, "medicine_id": 1, "usable_stock": 100.0},
    ]
    batches = [
        {
            "id": 101,
            "facility_id": 1,
            "medicine_id": 1,
            "batch_number": "BATCH-DONOR-01",
            "expiry_date": today + timedelta(days=180),
            "quantity_remaining": 1500.0,
            "unit_cost_etb": 2.50,
            "status": "Active",
        }
    ]

    result = optimizer.solve(facilities, medicines, inventories, batches, today=today)

    assert result["solver_status"] in ["OPTIMAL", "FEASIBLE", "HEURISTIC_OPTIMAL"]
    assert len(result["allocations"]) == 1

    alloc = result["allocations"][0]
    assert alloc["source_facility_id"] == 1
    assert alloc["target_facility_id"] == 2
    # Recipient deficit was 400 units, so optimal transfer is exactly 400 units
    assert alloc["quantity_recommended"] == 400.0
    assert result["total_transferred_units"] == 400.0
    assert result["net_benefit_etb"] > 0.0


def test_milp_safety_stock_protection():
    optimizer = MILPRedistributionOptimizer()
    today = date.today()

    # Donor has NO surplus (usable_stock = 400 < minimum_stock_level = 500)
    facilities = [
        {"id": 1, "name": "Donor", "latitude": 9.00, "longitude": 38.70},
        {"id": 2, "name": "Recipient", "latitude": 9.04, "longitude": 38.73},
    ]
    medicines = [{"id": 1, "name": "Amoxicillin", "minimum_stock_level": 500.0}]
    inventories = [
        {"id": 1, "facility_id": 1, "medicine_id": 1, "usable_stock": 400.0},
        {"id": 2, "facility_id": 2, "medicine_id": 1, "usable_stock": 50.0},
    ]
    batches = [
        {
            "id": 101,
            "facility_id": 1,
            "medicine_id": 1,
            "batch_number": "B1",
            "expiry_date": today + timedelta(days=120),
            "quantity_remaining": 400.0,
            "unit_cost_etb": 2.0,
            "status": "Active",
        }
    ]

    result = optimizer.solve(facilities, medicines, inventories, batches, today=today)
    # Hard constraint: Must NOT allocate stock from donor without surplus
    assert len(result["allocations"]) == 0
    assert result["total_transferred_units"] == 0.0


# ──────────────────────────────────────────────────────────────
# 3. Simulation Scenarios Tests
# ──────────────────────────────────────────────────────────────

def test_simulation_scenarios():
    simulator = RedistributionSimulator()
    today = date.today()

    facilities = [
        {"id": 1, "name": "Donor Central", "latitude": 9.00, "longitude": 38.70},
        {"id": 2, "name": "Recipient Rural", "latitude": 9.03, "longitude": 38.72},
    ]
    medicines = [{"id": 1, "name": "Amoxicillin", "category": "Antibiotics", "minimum_stock_level": 600.0}]
    inventories = [
        {"id": 1, "facility_id": 1, "medicine_id": 1, "usable_stock": 2500.0},
        {"id": 2, "facility_id": 2, "medicine_id": 1, "usable_stock": 50.0},
    ]
    batches = [
        {
            "id": 1,
            "facility_id": 1,
            "medicine_id": 1,
            "expiry_date": today + timedelta(days=150),
            "quantity_remaining": 1500.0,
            "unit_cost_etb": 3.0,
            "status": "Active",
        }
    ]

    # Test collaborative network scenario
    collab = simulator.run_scenario(
        scenario_type="collaborative_network",
        facilities=facilities,
        medicines=medicines,
        inventories=inventories,
        batches=batches,
    )
    assert collab["scenario_type"] == "collaborative_network"
    assert collab["improvement_summary"]["shortage_reduction_units"] > 0.0
    assert collab["scenario_kpis"]["service_level_percent"] >= collab["baseline_kpis"]["service_level_percent"]

    # Test epidemic spike scenario
    spike = simulator.run_scenario(
        scenario_type="epidemic_spike",
        facilities=facilities,
        medicines=medicines,
        inventories=inventories,
        batches=batches,
    )
    assert spike["scenario_type"] == "epidemic_spike"
    assert "outbreak" in spike["description"].lower() or "epidemic" in spike["description"].lower()


# ──────────────────────────────────────────────────────────────
# 4. Service Approval Lifecycle & Transfer Execution Tests
# ──────────────────────────────────────────────────────────────

def test_redistribution_service_full_lifecycle(db_session: Session):
    service = RedistributionService(db_session)

    # 1. Ensure second facility exists for inter-facility transfers
    fac2 = db_session.query(Facility).filter(Facility.code == "ETH-TEST-02").first()
    if not fac2:
        fac2 = Facility(
            code="ETH-TEST-02",
            name="St. Pauls Hospital Test",
            facility_type="Specialized Referral Hospital",
            region="Addis Ababa",
            latitude=9.04,
            longitude=38.73,
            is_active=True,
        )
        db_session.add(fac2)
        db_session.commit()

    # 2. Setup inventory: Facility 1 has 3000 units (surplus), Facility 2 has 50 units (deficit)
    inv1 = db_session.query(Inventory).filter(Inventory.facility_id == 1, Inventory.medicine_id == 1).first()
    if not inv1:
        inv1 = Inventory(facility_id=1, medicine_id=1, current_stock=3000.0, usable_stock=3000.0)
        db_session.add(inv1)
    else:
        inv1.current_stock = 3000.0
        inv1.usable_stock = 3000.0

    inv2 = db_session.query(Inventory).filter(Inventory.facility_id == fac2.id, Inventory.medicine_id == 1).first()
    if not inv2:
        inv2 = Inventory(facility_id=fac2.id, medicine_id=1, current_stock=50.0, usable_stock=50.0)
        db_session.add(inv2)
    else:
        inv2.current_stock = 50.0
        inv2.usable_stock = 50.0

    # Ensure batch exists at Facility 1
    batch = db_session.query(Batch).filter(Batch.facility_id == 1, Batch.medicine_id == 1).first()
    if not batch:
        batch = Batch(
            facility_id=1,
            medicine_id=1,
            batch_number="BATCH-LIFECYCLE-01",
            expiry_date=date.today() + timedelta(days=200),
            quantity_initial=2000.0,
            quantity_remaining=2000.0,
            unit_cost_etb=2.50,
            status="Active",
        )
        db_session.add(batch)
    else:
        batch.quantity_remaining = 2000.0
        batch.expiry_date = date.today() + timedelta(days=200)

    db_session.commit()

    # 3. Create recommendation directly
    rec = RedistributionRecommendation(
        source_facility_id=1,
        target_facility_id=fac2.id,
        medicine_id=1,
        batch_id=batch.id,
        quantity_recommended=300.0,
        transport_distance_km=4.2,
        estimated_transfer_cost_etb=65.0,
        prevented_wastage_cost_etb=750.0,
        status="Pending",
        priority="High",
        rationale="Lifecycle integration test recommendation.",
    )
    db_session.add(rec)
    db_session.commit()
    db_session.refresh(rec)

    # 4. Check Detail with Mathematical Proof
    detail = service.get_recommendation_detail(rec.id)
    assert detail.mathematical_proof is not None
    assert detail.mathematical_proof.net_economic_benefit_etb == pytest.approx(685.0, rel=1e-2)

    # 5. Approve recommendation -> Should reserve 300 units at donor
    approved = service.approve_recommendation(rec.id, user_id=1, rationale="Approved by chief pharmacist.")
    assert approved.status == "Approved"
    assert inv1.reserved_stock >= 300.0

    # 6. Execute transfer -> Moves stock physically and logs bin-card transactions
    executed = service.execute_transfer(rec.id, user_id=1)
    assert executed.status == "Completed"
    assert inv2.current_stock >= 350.0


# ──────────────────────────────────────────────────────────────
# 5. API Endpoints Integration Tests
# ──────────────────────────────────────────────────────────────

def test_api_redistribution_endpoints(client: TestClient):
    token = get_auth_token(client)

    # 1. Run optimization endpoint
    opt_res = client.post(
        "/api/v1/redistribution/optimize",
        headers={"Authorization": f"Bearer {token}"},
        json={"max_distance_km": 150.0, "min_expiry_months": 2},
    )
    assert opt_res.status_code == 200
    data = opt_res.json()
    assert isinstance(data, list)

    # 2. List recommendations
    list_res = client.get(
        "/api/v1/redistribution/recommendations",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert list_res.status_code == 200
    recs = list_res.json()
    assert len(recs) >= 1

    first_rec_id = recs[0]["id"]

    # 3. Get detail with mathematical proof
    detail_res = client.get(
        f"/api/v1/redistribution/recommendations/{first_rec_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert detail_res.status_code == 200
    assert "mathematical_proof" in detail_res.json()

    # 4. Run simulation endpoint
    sim_res = client.post(
        "/api/v1/redistribution/simulate",
        headers={"Authorization": f"Bearer {token}"},
        json={"scenario_type": "collaborative_network", "horizon_months": 6},
    )
    assert sim_res.status_code == 200
    sim_data = sim_res.json()
    assert sim_data["scenario_type"] == "collaborative_network"
    assert "improvement_summary" in sim_data

