"""
PharmaIntelligence AI - Clinical Lateral Redistribution Lifecycle Integration Test

Validates the complete end-to-end clinical operational journey:
1. Stock Sheet Ingestion: Recipient facility uploads physical inventory CSV count.
2. DSR Detection: System evaluates Days of Stock Remaining (DSR) and flags acute stockout risk.
3. MILP Lateral Transfer Formulation: PuLP optimizer pairs donor surplus with recipient deficit.
4. Pharmacist Clinical Approval: Pharmacy manager approves transfer with mandatory clinical justification.
5. Consignment Note / Waybill Verification: Tripartite chain-of-custody consignment fields & proof.
6. Ledger Bin-Card Update & Physical Execution: Stock movement, TRANSFER_IN / TRANSFER_OUT transactions.
"""

import io
import pytest
from datetime import date, datetime, timedelta, timezone
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models.user import User
from app.models.role import Role
from app.models.facility import Facility
from app.models.medicine import Medicine
from app.models.inventory import Inventory
from app.models.batch import Batch
from app.models.transaction import InventoryTransaction
from app.models.audit_log import AuditLog
from app.models.recommendation import RedistributionRecommendation


@pytest.fixture
def clinical_flow_context(db_session: Session):
    """Sets up donor and recipient tertiary hospitals, medicine, users, and baseline donor surplus."""
    # Ensure roles exist
    admin_role = db_session.query(Role).filter_by(name="admin").first()
    if not admin_role:
        admin_role = Role(name="admin", description="System Administrator")
        db_session.add(admin_role)

    manager_role = db_session.query(Role).filter_by(name="pharmacy_manager").first()
    if not manager_role:
        manager_role = Role(name="pharmacy_manager", description="Hospital Pharmacy Manager")
        db_session.add(manager_role)
    db_session.flush()

    # 1. Donor Facility: Tikur Anbessa Specialized Hospital (Surplus Center)
    donor_facility = Facility(
        code="ETH-FLOW-DONOR",
        name="Tikur Anbessa Specialized Hospital (Donor Center)",
        facility_type="Specialized Referral Hospital",
        region="Addis Ababa",
        latitude=9.0142,
        longitude=38.7525,
        storage_capacity_m3=1500.0,
        is_active=True,
    )
    db_session.add(donor_facility)

    # 2. Recipient Facility: St. Paul's Hospital MMC (Deficit Center)
    recipient_facility = Facility(
        code="ETH-FLOW-RECIP",
        name="St. Paul's Hospital MMC (Recipient Deficit Center)",
        facility_type="Teaching & Referral Hospital",
        region="Addis Ababa",
        latitude=9.0567,
        longitude=38.7297,
        storage_capacity_m3=1200.0,
        is_active=True,
    )
    db_session.add(recipient_facility)
    db_session.flush()

    # 3. Essential NEML Medicine: Amoxicillin 500mg Capsule
    amoxicillin = Medicine(
        code="MED-FLOW-AMX500",
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
    db_session.add(amoxicillin)
    db_session.flush()

    # 4. Donor Baseline Inventory & Surplus Batch (3,500 units, 240 days to expiry)
    donor_inventory = Inventory(
        facility_id=donor_facility.id,
        medicine_id=amoxicillin.id,
        current_stock=3500.0,
        reserved_stock=0.0,
        usable_stock=3500.0,
        average_monthly_consumption=250.0,
        months_of_stock=14.0,
        stock_status="Adequate",
    )
    db_session.add(donor_inventory)

    donor_batch = Batch(
        facility_id=donor_facility.id,
        medicine_id=amoxicillin.id,
        batch_number="FLOW-BATCH-DONOR-SURPLUS",
        manufacturing_date=date.today() - timedelta(days=90),
        expiry_date=date.today() + timedelta(days=240),
        quantity_initial=3500.0,
        quantity_remaining=3500.0,
        unit_cost_etb=26.0,
        status="Active",
    )
    db_session.add(donor_batch)

    # 5. Create Pharmacy Manager User (Clinical Approver)
    pharmacist = User(
        email="clinical_pharmacist@pharmaintelligence.et",
        full_name="Dr. Tigist Mengistu (Chief Pharmacist)",
        hashed_password=get_password_hash("ClinicalPass123!"),
        is_active=True,
        role_id=manager_role.id,
        facility_id=recipient_facility.id,
    )
    db_session.add(pharmacist)

    # 6. Create Admin / Logistics Coordinator User
    admin = User(
        email="logistics_admin@pharmaintelligence.et",
        full_name="Abebe Balcha (Supply Chain Director)",
        hashed_password=get_password_hash("LogisticsPass123!"),
        is_active=True,
        role_id=admin_role.id,
        facility_id=donor_facility.id,
    )
    db_session.add(admin)
    db_session.commit()

    return {
        "donor_facility": donor_facility,
        "recipient_facility": recipient_facility,
        "medicine": amoxicillin,
        "donor_batch": donor_batch,
        "donor_inventory": donor_inventory,
        "pharmacist": pharmacist,
        "admin": admin,
    }


def test_complete_clinical_transfer_journey(client: TestClient, clinical_flow_context, db_session: Session):
    """
    Executes and validates the complete clinical journey:
    1. Ingest stock sheet -> 2. Detect low DSR -> 3. Formulate lateral transfer ->
    4. Pharmacist approval -> 5. Consignment Waybill -> 6. Ledger update.
    """
    donor_fac = clinical_flow_context["donor_facility"]
    recip_fac = clinical_flow_context["recipient_facility"]
    medicine = clinical_flow_context["medicine"]
    pharmacist = clinical_flow_context["pharmacist"]
    admin = clinical_flow_context["admin"]

    # Authenticate Admin (Supply Chain Officer)
    admin_login = client.post(
        "/api/v1/auth/login/json",
        json={"email": admin.email, "password": "LogisticsPass123!"},
    )
    assert admin_login.status_code == 200, "Admin login failed"
    admin_token = admin_login.json()["token"]["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    # Authenticate Clinical Pharmacist
    pharm_login = client.post(
        "/api/v1/auth/login/json",
        json={"email": pharmacist.email, "password": "ClinicalPass123!"},
    )
    assert pharm_login.status_code == 200, "Pharmacist login failed"
    pharm_token = pharm_login.json()["token"]["access_token"]
    pharm_headers = {"Authorization": f"Bearer {pharm_token}"}

    # =========================================================================
    # STEP 1: Ingest stock sheet (Physical inventory count upload)
    # =========================================================================
    # Recipient facility submits bin-card physical count reporting critically depleted stock of 30 units
    csv_stock_sheet = (
        b"medicine_code,batch_number,expiry_date,quantity,unit_cost_etb\n"
        b"MED-FLOW-AMX500,RECIP-DEPLETED-LOT-01,2026-12-31,30,26.50\n"
    )

    import_resp = client.post(
        "/api/v1/imports/inventory-batches",
        headers=admin_headers,
        data={"facility_id": recip_fac.id},
        files={"file": ("st_pauls_stock_sheet.csv", io.BytesIO(csv_stock_sheet), "text/csv")},
    )
    assert import_resp.status_code == 200, f"Stock sheet import failed: {import_resp.text}"
    import_result = import_resp.json()
    assert import_result["valid_rows"] == 1, "Expected 1 valid ingested row"
    assert import_result["rejected_rows"] == 0, "Expected 0 rejected rows"
    assert import_result["status"] == "COMPLETED", "Import status should be COMPLETED"

    # Verify database reconciliation: recipient inventory reflects 30 units
    recip_inv_db = db_session.query(Inventory).filter(
        Inventory.facility_id == recip_fac.id,
        Inventory.medicine_id == medicine.id,
    ).first()
    assert recip_inv_db is not None, "Recipient inventory record must exist post-ingestion"
    assert recip_inv_db.current_stock == 30.0, "Current stock must match uploaded count (30 units)"
    assert recip_inv_db.usable_stock == 30.0

    # Ensure recipient AMC is set to 300 units/mo (~10 units/day) for realistic clinical burn-down
    recip_inv_db.average_monthly_consumption = 300.0
    recip_inv_db.stock_status = "Understocked"
    db_session.commit()

    # =========================================================================
    # STEP 2: Detect low DSR (Days of Stock Remaining) & acute stockout risk
    # =========================================================================
    # 30 units on hand / 10 units/day consumption = 3.0 Days of Stock Remaining (DSR)
    # Lead time is 25 days -> Acute stockout risk within < 4 days!
    stockout_resp = client.get(
        f"/api/v1/stockout/facilities/{recip_fac.id}",
        headers=admin_headers,
    )
    assert stockout_resp.status_code == 200, f"Stockout evaluation failed: {stockout_resp.text}"
    stockout_items = stockout_resp.json()
    assert len(stockout_items) >= 1, "Must return evaluated risk for recipient medicines"

    amx_risk = next((r for r in stockout_items if r["medicine_id"] == medicine.id), None)
    assert amx_risk is not None, "Amoxicillin must be present in stockout evaluation"

    # Clinical DSR assertions
    dsr = amx_risk["days_until_stockout"]
    assert dsr <= 10.0, f"DSR must be critical (< 10 days), got {dsr}"
    assert amx_risk["risk_level"] in ["Critical", "High"], f"Risk level must be Critical or High, got {amx_risk['risk_level']}"
    assert amx_risk["stockout_risk_score"] >= 0.70, "Stockout probability must reflect acute shortage"
    assert "attributions" in amx_risk, "XAI attributions must explain risk score"
    assert len(amx_risk["attributions"]) > 0, "Must have TreeSHAP feature attributions"

    # =========================================================================
    # STEP 3: Formulate lateral transfer (MILP optimization solver)
    # =========================================================================
    # Supply chain coordinator runs MILP optimization with road distance and buffer constraints
    opt_resp = client.post(
        "/api/v1/redistribution/optimize",
        headers=admin_headers,
        json={
            "max_distance_km": 150.0,
            "min_expiry_months": 2,
            "cost_shortage_penalty": 100.0,
            "cost_waste_penalty": 50.0,
            "cost_transport_per_km_unit": 0.05,
        },
    )
    assert opt_resp.status_code == 200, f"Optimization run failed: {opt_resp.text}"
    recommendations = opt_resp.json()
    assert len(recommendations) >= 1, "MILP solver must formulate at least one transfer"

    # Locate the lateral transfer from Donor Hospital to Recipient Hospital
    transfer_proposal = next(
        (p for p in recommendations if p["source_facility_id"] == donor_fac.id and p["target_facility_id"] == recip_fac.id),
        recommendations[0],
    )
    assert transfer_proposal["status"] == "Pending", "Newly formulated proposal must be in Pending status"
    assert transfer_proposal["quantity_recommended"] > 0, "Recommended transfer quantity must be positive"
    assert transfer_proposal["prevented_wastage_cost_etb"] > 0, "Must calculate positive financial value preserved"
    recommendation_id = transfer_proposal["id"]

    # =========================================================================
    # STEP 4: Pharmacist clinical approval
    # =========================================================================
    # Chief Pharmacist reviews the clinical recommendation and issues approval with clinical justification
    clinical_rationale = (
        "Approved by Clinical Pharmacy Director: Verified emergency pediatric deficit at St. Paul's triage. "
        "Donor buffer at Tikur Anbessa remains above 90-day threshold."
    )
    approve_resp = client.patch(
        f"/api/v1/redistribution/recommendations/{recommendation_id}/approve",
        headers=pharm_headers,
        json={"status": "Approved", "rationale": clinical_rationale},
    )
    assert approve_resp.status_code == 200, f"Pharmacist approval failed: {approve_resp.text}"
    approved_data = approve_resp.json()
    assert approved_data["status"] == "Approved", "Status must update to Approved"
    assert approved_data["reviewed_by"] == pharmacist.id, "Reviewer ID must match approving pharmacist"

    # Verify donor inventory reserves stock upon approval to prevent double-allocation
    db_session.expire_all()
    donor_inv_after_approval = db_session.query(Inventory).filter(
        Inventory.facility_id == donor_fac.id,
        Inventory.medicine_id == medicine.id,
    ).first()
    assert donor_inv_after_approval.reserved_stock >= transfer_proposal["quantity_recommended"]
    assert donor_inv_after_approval.usable_stock == (
        donor_inv_after_approval.current_stock - donor_inv_after_approval.reserved_stock
    )

    # Verify audit log captures the approval event
    approval_audit = db_session.query(AuditLog).filter(
        AuditLog.action == "APPROVE_REDISTRIBUTION",
        AuditLog.entity_id == str(recommendation_id),
    ).first()
    assert approval_audit is not None, "Audit log must record APPROVE_REDISTRIBUTION"
    assert approval_audit.user_id == pharmacist.id

    # =========================================================================
    # STEP 5: Consignment Note / Waybill Verification
    # =========================================================================
    # Generate and verify official Ethiopian Health Lateral Stock Transfer Consignment Note
    detail_resp = client.get(
        f"/api/v1/redistribution/recommendations/{recommendation_id}",
        headers=admin_headers,
    )
    assert detail_resp.status_code == 200, f"Waybill detail fetch failed: {detail_resp.text}"
    waybill_data = detail_resp.json()

    # Validate official consignment note fields
    assert waybill_data["id"] == recommendation_id
    assert waybill_data["source_facility_id"] == donor_fac.id
    assert waybill_data["target_facility_id"] == recip_fac.id
    assert waybill_data["medicine_id"] == medicine.id
    assert waybill_data["quantity_recommended"] == transfer_proposal["quantity_recommended"]
    assert waybill_data["transport_distance_km"] > 0
    assert waybill_data["estimated_transfer_cost_etb"] > 0
    assert waybill_data["prevented_wastage_cost_etb"] > 0

    # Validate mathematical proof embedded in consignment note
    proof = waybill_data.get("mathematical_proof")
    assert proof is not None, "Mathematical proof must be present in consignment note"
    assert "donor_surplus_proof" in proof
    assert "recipient_deficit_proof" in proof
    assert "distance_proof" in proof
    assert proof["net_economic_benefit_etb"] > 0

    # =========================================================================
    # STEP 6: Ledger update & physical stock transfer execution
    # =========================================================================
    # Physical stock is dispatched and received, updating electronic bin-card ledgers
    pre_donor_stock = donor_inv_after_approval.current_stock
    pre_recip_stock = recip_inv_db.current_stock
    transfer_qty = transfer_proposal["quantity_recommended"]

    exec_resp = client.post(
        f"/api/v1/redistribution/recommendations/{recommendation_id}/execute",
        headers=admin_headers,
    )
    assert exec_resp.status_code == 200, f"Transfer execution failed: {exec_resp.text}"
    exec_data = exec_resp.json()
    assert exec_data["status"] == "Completed", "Status must transition to Completed"

    # Refresh DB state
    db_session.expire_all()

    # 1. Verify physical inventory balances
    final_donor_inv = db_session.query(Inventory).filter(
        Inventory.facility_id == donor_fac.id,
        Inventory.medicine_id == medicine.id,
    ).first()
    final_recip_inv = db_session.query(Inventory).filter(
        Inventory.facility_id == recip_fac.id,
        Inventory.medicine_id == medicine.id,
    ).first()

    assert final_donor_inv.current_stock == pre_donor_stock - transfer_qty, "Donor stock must be decremented by transfer qty"
    assert final_donor_inv.reserved_stock == 0.0, "Donor reserved stock must be released after completion"
    assert final_recip_inv.current_stock == pre_recip_stock + transfer_qty, "Recipient stock must be incremented by transfer qty"
    assert final_recip_inv.usable_stock == pre_recip_stock + transfer_qty, "Recipient usable stock must reflect new units"

    # 2. Verify bin-card ledger transactions
    tx_out = db_session.query(InventoryTransaction).filter(
        InventoryTransaction.facility_id == donor_fac.id,
        InventoryTransaction.medicine_id == medicine.id,
        InventoryTransaction.transaction_type == "TRANSFER_OUT",
    ).first()
    assert tx_out is not None, "Bin-card TRANSFER_OUT transaction must be recorded at donor facility"
    assert tx_out.quantity == transfer_qty
    assert f"TRANSFER-REC-{recommendation_id}" in tx_out.reference_number

    tx_in = db_session.query(InventoryTransaction).filter(
        InventoryTransaction.facility_id == recip_fac.id,
        InventoryTransaction.medicine_id == medicine.id,
        InventoryTransaction.transaction_type == "TRANSFER_IN",
    ).first()
    assert tx_in is not None, "Bin-card TRANSFER_IN transaction must be recorded at recipient facility"
    assert tx_in.quantity == transfer_qty
    assert f"TRANSFER-REC-{recommendation_id}" in tx_in.reference_number

    # 3. Post-transfer DSR recovery verification
    # Recipient stock has increased from 30 units to (30 + transfer_qty)
    # Recipient DSR is now healthy (> 25 days)
    post_transfer_stockout_resp = client.get(
        f"/api/v1/stockout/facilities/{recip_fac.id}",
        headers=admin_headers,
    )
    assert post_transfer_stockout_resp.status_code == 200
    post_stockout_items = post_transfer_stockout_resp.json()
    amx_post_risk = next((r for r in post_stockout_items if r["medicine_id"] == medicine.id), None)
    if amx_post_risk:
        assert amx_post_risk["days_until_stockout"] > dsr, "DSR must significantly increase after transfer receipt"
