"""
PharmaIntelligence AI - End-to-End System Integration Tests

Connects authentication, database, data engineering, AI inference,
and redistribution optimization across a complete operational journey.
"""

import io
import pytest
from datetime import date, datetime, timedelta, timezone
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import create_access_token, get_password_hash
from app.models.user import User
from app.models.role import Role
from app.models.facility import Facility
from app.models.medicine import Medicine
from app.models.inventory import Inventory
from app.models.batch import Batch


@pytest.fixture
def e2e_system_context(db_session: Session):
    """Initializes interconnected facilities, medicines, and initial stocks for E2E testing."""
    admin_role = db_session.query(Role).filter_by(name="admin").first()
    if not admin_role:
        admin_role = Role(name="admin", description="System Administrator")
        db_session.add(admin_role)
        db_session.flush()

    # Facility 1: Donor (Addis Ababa)
    donor_fac = Facility(
        code="ETH-E2E-DONOR",
        name="E2E Donor Hospital",
        facility_type="Specialized Referral Hospital",
        region="Addis Ababa",
        latitude=9.05,
        longitude=38.73,
        storage_capacity_m3=1000.0,
        is_active=True,
    )
    db_session.add(donor_fac)

    # Facility 2: Recipient (Addis Ababa)
    recip_fac = Facility(
        code="ETH-E2E-RECIP",
        name="E2E Recipient Hospital",
        facility_type="Specialized Referral Hospital",
        region="Addis Ababa",
        latitude=9.01,
        longitude=38.75,
        storage_capacity_m3=1200.0,
        is_active=True,
    )
    db_session.add(recip_fac)
    db_session.flush()

    # Essential Medicine: Amoxicillin 500mg
    med = Medicine(
        code="MED-E2E-AMX",
        name="Amoxicillin 500mg Capsule",
        category="Anti-infectives",
        dosage_form="Capsule",
        strength="500mg",
        unit_of_measure="100 Capsules/Pack",
        is_essential=True,
        vital_classification="Vital",
        minimum_stock_level=500.0,
        reorder_point=1200.0,
        lead_time_days=25,
    )
    db_session.add(med)
    db_session.flush()

    # Donor inventory: Surplus of 4,000 units
    donor_inv = Inventory(
        facility_id=donor_fac.id,
        medicine_id=med.id,
        current_stock=4000.0,
        reserved_stock=0.0,
        usable_stock=4000.0,
        average_monthly_consumption=200.0,
        months_of_stock=20.0,
        stock_status="Adequate",
    )
    db_session.add(donor_inv)

    # Donor batch: Healthy shelf-life of 200 days
    donor_batch = Batch(
        facility_id=donor_fac.id,
        medicine_id=med.id,
        batch_number="E2E-BATCH-SURPLUS-01",
        manufacturing_date=date.today() - timedelta(days=60),
        expiry_date=date.today() + timedelta(days=200),
        quantity_initial=4000.0,
        quantity_remaining=4000.0,
        unit_cost_etb=25.0,
        status="Active",
    )
    db_session.add(donor_batch)

    # Recipient inventory: Critical deficit / stockout
    recip_inv = Inventory(
        facility_id=recip_fac.id,
        medicine_id=med.id,
        current_stock=50.0,
        reserved_stock=0.0,
        usable_stock=50.0,
        average_monthly_consumption=300.0,
        months_of_stock=0.17,
        stock_status="Understocked",
    )
    db_session.add(recip_inv)

    # Recipient batch: Near expiry
    recip_batch = Batch(
        facility_id=recip_fac.id,
        medicine_id=med.id,
        batch_number="E2E-BATCH-DEPLETED-01",
        manufacturing_date=date.today() - timedelta(days=300),
        expiry_date=date.today() + timedelta(days=20),
        quantity_initial=500.0,
        quantity_remaining=50.0,
        unit_cost_etb=25.0,
        status="Active",
    )
    db_session.add(recip_batch)

    # Create admin user
    admin_user = User(
        email="e2e_admin@pharmaintelligence.et",
        full_name="E2E National Admin",
        hashed_password=get_password_hash("Admin123!Secure"),
        is_active=True,
        role_id=admin_role.id,
        facility_id=donor_fac.id,
    )
    db_session.add(admin_user)
    db_session.commit()

    return {
        "admin": admin_user,
        "donor_fac": donor_fac,
        "recip_fac": recip_fac,
        "medicine": med,
        "donor_batch": donor_batch,
    }


def test_end_to_end_supply_chain_lifecycle(client: TestClient, e2e_system_context):
    """
    Executes the complete end-to-end integration flow:
    1. Auth Login (JSON SPA format)
    2. Import Preview validation
    3. 5D Data Quality Assessment
    4. Probabilistic Stockout Risk Inference + XAI
    5. FEFO Expiry Simulation & Financial Loss
    6. Multi-model Demand Forecasting & Algorithm Benchmark
    7. MILP Redistribution Optimization
    8. Transfer Proposal Approval & Execution
    9. System Summary & Report Metrics
    """
    admin = e2e_system_context["admin"]
    donor_fac = e2e_system_context["donor_fac"]
    recip_fac = e2e_system_context["recip_fac"]
    med = e2e_system_context["medicine"]

    # 1. Auth Login
    login_resp = client.post(
        "/api/v1/auth/login/json",
        json={"email": admin.email, "password": "Admin123!Secure"},
    )
    assert login_resp.status_code == 200
    token = login_resp.json()["token"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Verify /me endpoint
    me_resp = client.get("/api/v1/auth/me", headers=headers)
    assert me_resp.status_code == 200
    assert me_resp.json()["email"] == admin.email

    # 2. Ingestion Pre-Flight Inspection (CSV upload preview)
    csv_content = (
        b"facility_code,medicine_code,batch_number,expiry_date,quantity,unit_cost\n"
        b"ETH-E2E-RECIP,MED-E2E-AMX,E2E-CSV-LOT-01,2027-01-01,500,24.50\n"
    )
    preview_resp = client.post(
        "/api/v1/imports/preview",
        headers=headers,
        files={"file": ("inventory.csv", io.BytesIO(csv_content), "text/csv")},
        data={"preview_limit": 5},
    )
    assert preview_resp.status_code == 200
    assert preview_resp.json()["total_rows"] == 1
    assert preview_resp.json()["preliminary_dq_score"] >= 80.0

    # 3. 5D Data Quality Assessment
    dqi_resp = client.get(
        f"/api/v1/data-quality/facilities/{recip_fac.id}/assessment",
        headers=headers,
    )
    assert dqi_resp.status_code == 200
    dqi_data = dqi_resp.json()
    assert "dqi_score" in dqi_data
    assert "dimensions" in dqi_data
    assert dqi_data["dqi_score"] > 70.0

    # 4. Probabilistic Stockout Risk Intelligence
    stockout_resp = client.get(
        f"/api/v1/stockout/facilities/{recip_fac.id}",
        headers=headers,
    )
    assert stockout_resp.status_code == 200
    stockout_list = stockout_resp.json()
    assert len(stockout_list) >= 1
    recip_stockout = stockout_list[0]
    assert recip_stockout["risk_level"] in ["Critical", "High"]
    assert "attributions" in recip_stockout
    assert len(recip_stockout["attributions"]) > 0

    # 5. FEFO Expiry Risk Intelligence
    expiry_resp = client.get(
        f"/api/v1/expiry/facilities/{recip_fac.id}",
        headers=headers,
    )
    assert expiry_resp.status_code == 200
    expiry_list = expiry_resp.json()
    assert len(expiry_list) >= 1
    assert "quantity_at_risk" in expiry_list[0]
    assert "estimated_loss_etb" in expiry_list[0]

    # 6. Demand Forecasting Hub
    forecast_resp = client.get(
        f"/api/v1/forecasting/facilities/{recip_fac.id}/medicines/{med.id}?horizon_days=60&model_type=ensemble",
        headers=headers,
    )
    assert forecast_resp.status_code == 200
    forecast_data = forecast_resp.json()
    assert "forecast_value" in forecast_data
    assert "series" in forecast_data

    # Algorithm Comparison
    compare_resp = client.get(
        f"/api/v1/forecasting/facilities/{recip_fac.id}/medicines/{med.id}/compare",
        headers=headers,
    )
    assert compare_resp.status_code == 200
    compare_data = compare_resp.json()
    assert "demand_category" in compare_data
    assert len(compare_data["models_evaluated"]) >= 3

    # 7. MILP Lateral Redistribution Optimization
    opt_resp = client.post(
        "/api/v1/redistribution/optimize",
        headers=headers,
        json={
            "max_transport_distance_km": 50.0,
            "donor_safety_stock_days": 30.0,
            "cost_transport_per_km_unit": 0.02,
        },
    )
    assert opt_resp.status_code == 200
    proposals = opt_resp.json()
    assert len(proposals) >= 1

    proposal = proposals[0]
    assert proposal["status"] == "Pending"
    assert proposal["quantity_recommended"] > 0
    assert proposal["prevented_wastage_cost_etb"] > 0

    # 8. Clinical Approval & Execution Lifecycle
    approve_resp = client.patch(
        f"/api/v1/redistribution/recommendations/{proposal['id']}/approve",
        headers=headers,
        json={"status": "Approved", "rationale": "E2E automated approval for urgent stockout relief"},
    )
    assert approve_resp.status_code == 200
    assert approve_resp.json()["status"] == "Approved"

    exec_resp = client.post(
        f"/api/v1/redistribution/recommendations/{proposal['id']}/execute",
        headers=headers,
    )
    assert exec_resp.status_code == 200
    assert exec_resp.json()["status"] == "Completed"

    # 9. Executive Reports & System Summary
    summary_resp = client.get(
        "/api/v1/reports/summary",
        headers=headers,
    )
    assert summary_resp.status_code == 200
    summary_data = summary_resp.json()
    assert summary_data["total_facilities"] >= 2
    assert summary_data["total_inventory_items"] >= 2
