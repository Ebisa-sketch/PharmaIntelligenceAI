import io
import json
import pytest
from datetime import date, datetime, timedelta, timezone
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import Batch, Inventory, InventoryTransaction, DataImport, DataQualityIssue
from app.services.import_service import ImportService
from app.services.data_quality_service import DataQualityService
from data.synthetic.generators.synthetic_generator import SyntheticDataGenerator


def get_auth_token(client: TestClient):
    res = client.post(
        "/api/v1/auth/login/json",
        json={"email": "dataadmin@pharmaintelligence.et", "password": "DataAdminSecret123!"},
    )
    return res.json()["token"]["access_token"]


# ──────────────────────────────────────────────────────────────
# 1. Synthetic Data Generator Tests
# ──────────────────────────────────────────────────────────────

def test_synthetic_generator_generation():
    generator = SyntheticDataGenerator(
        num_facilities=2,
        num_months=12,
        anomaly_rate=0.04,
        seed=101,
    )
    dataset = generator.generate_full_dataset()
    metadata = dataset["metadata"]

    assert metadata["num_facilities"] == 2
    assert metadata["num_medicines"] == 10
    assert metadata["num_batches"] > 0
    assert metadata["num_transactions"] > 0
    assert metadata["num_inventory_records"] == 20
    assert metadata["anomalies_count"] > 0

    # Test CSV export
    batch_csv = generator.export_batches_csv(dataset["batches"][:10])
    assert "medicine_code,batch_number,expiry_date,quantity" in batch_csv

    tx_csv = generator.export_transactions_csv(dataset["transactions"][:10])
    assert "medicine_code,transaction_type,quantity,transaction_date" in tx_csv


# ──────────────────────────────────────────────────────────────
# 2. Import Service Tests
# ──────────────────────────────────────────────────────────────

def test_import_service_preview(db_session: Session):
    service = ImportService(db_session)

    csv_data = (
        "medicine_code,batch_number,expiry_date,quantity,unit_cost_etb\n"
        "MED-AMOX-500,BATCH-001,2028-01-01,1000,2.50\n"
        "MED-AMOX-500,BATCH-002,2028-02-01,-50,2.50\n"
        "UNKNOWN-MED,BATCH-003,2028-03-01,500,1.20\n"
    ).encode("utf-8")

    preview = service.preview_import(csv_data, "test_preview.csv")
    assert preview["total_rows"] == 3
    assert "medicine_code" in preview["detected_headers"]
    assert len(preview["sample_rows"]) == 3


def test_import_service_inventory_batches_workflow(db_session: Session):
    service = ImportService(db_session)

    csv_data = (
        "medicine_code,batch_number,expiry_date,quantity,unit_cost_etb\n"
        "MED-AMOX-500,BATCH-TASH-01,2028-06-30,2500,2.40\n"
        "MED-PARA-500,BATCH-TASH-02,2027-12-31,5000,0.80\n"
        "UNKNOWN-CODE,BATCH-TASH-03,2028-01-01,100,1.00\n"
    ).encode("utf-8")

    result = service.import_inventory_batches(
        file_bytes=csv_data,
        filename="test_batches.csv",
        facility_id=1,
        user_id=1,
    )

    assert result["total_rows"] == 3
    assert result["valid_rows"] == 2
    assert result["rejected_rows"] == 1
    assert result["dq_score"] == pytest.approx(66.7, rel=1e-1)
    assert result["status"] == "PARTIAL_SUCCESS"

    # Verify database updates
    batch = db_session.query(Batch).filter(Batch.batch_number == "BATCH-TASH-01").first()
    assert batch is not None
    assert batch.quantity_remaining == 2500.0

    inventory = db_session.query(Inventory).filter(Inventory.facility_id == 1, Inventory.medicine_id == batch.medicine_id).first()
    assert inventory is not None
    assert inventory.current_stock >= 2500.0


def test_import_service_transactions_workflow(db_session: Session):
    service = ImportService(db_session)

    csv_data = (
        "medicine_code,transaction_type,quantity,transaction_date,batch_number,notes\n"
        "MED-AMOX-500,DISPENSATION,150,2026-03-01,BATCH-TASH-01,OPD prescription\n"
        "MED-PARA-500,RECEIPT,2000,2026-03-02,BATCH-TASH-02,Central replenishment\n"
        "MED-PARA-500,INVALID_TYPE,500,2026-03-03,BATCH-TASH-02,Bad row\n"
    ).encode("utf-8")

    result = service.import_transactions(
        file_bytes=csv_data,
        filename="test_transactions.csv",
        facility_id=1,
        user_id=1,
    )

    assert result["total_rows"] == 3
    assert result["valid_rows"] == 2
    assert result["rejected_rows"] == 1

    txs = db_session.query(InventoryTransaction).filter(InventoryTransaction.facility_id == 1).all()
    assert len(txs) >= 2


# ──────────────────────────────────────────────────────────────
# 3. Data Quality Service Tests
# ──────────────────────────────────────────────────────────────

def test_data_quality_service_assessment(db_session: Session):
    service = DataQualityService(db_session)

    # Ingest a deliberate data quality flaw: expired active batch
    expired_batch = Batch(
        facility_id=1,
        medicine_id=1,
        batch_number="EXPIRED-BATCH-99",
        expiry_date=date.today() - timedelta(days=60),
        quantity_initial=300,
        quantity_remaining=300,
        status="Active",
    )
    db_session.add(expired_batch)
    db_session.commit()

    assessment = service.assess_facility_data_quality(facility_id=1, persist_issues=True)

    assert assessment["facility_id"] == 1
    assert assessment["dqi_score"] < 100.0
    assert len(assessment["dimensions"]) == 5
    assert assessment["total_issues"] > 0

    # Ensure Expiry Validity flagged the expired active batch
    expiry_dim = next(d for d in assessment["dimensions"] if d["dimension"] == "Expiry Validity")
    assert expiry_dim["issue_count"] >= 1


def test_data_quality_issue_resolution(db_session: Session):
    service = DataQualityService(db_session)

    issues = service.get_quality_issues(facility_id=1, is_resolved=False)
    assert len(issues) > 0

    first_issue_id = issues[0].id
    resolved = service.resolve_issue(first_issue_id, notes="Manually quarantined batch.")

    assert resolved is not None
    assert resolved.is_resolved is True
    assert "[Resolution]: Manually quarantined batch." in resolved.details


# ──────────────────────────────────────────────────────────────
# 4. API Endpoints Integration Tests
# ──────────────────────────────────────────────────────────────

def test_api_import_preview(client: TestClient):
    token = get_auth_token(client)
    file_bytes = (
        "medicine_code,batch_number,expiry_date,quantity,unit_cost_etb\n"
        "MED-AMOX-500,PREVIEW-01,2028-10-10,300,2.50\n"
    ).encode("utf-8")

    res = client.post(
        "/api/v1/imports/preview",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("test_preview.csv", io.BytesIO(file_bytes), "text/csv")},
        data={"preview_limit": 5},
    )

    assert res.status_code == 200
    data = res.json()
    assert data["total_rows"] == 1
    assert data["preliminary_dq_score"] == 100.0


def test_api_data_quality_assessment_endpoint(client: TestClient):
    token = get_auth_token(client)
    res = client.get(
        "/api/v1/data-quality/facilities/1/assessment?persist=true",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert res.status_code == 200
    data = res.json()
    assert "dqi_score" in data
    assert "dimensions" in data
    assert len(data["dimensions"]) == 5


def test_api_data_quality_issues_list_and_resolve(client: TestClient):
    token = get_auth_token(client)
    # List issues
    res = client.get(
        "/api/v1/data-quality/issues?facility_id=1",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    issues = res.json()
    assert len(issues) >= 1

    issue_id = issues[0]["id"]
    # Resolve issue
    resolve_res = client.patch(
        f"/api/v1/data-quality/issues/{issue_id}/resolve",
        headers={"Authorization": f"Bearer {token}"},
        json={"resolved": True, "resolution_notes": "Reviewed and verified."},
    )
    assert resolve_res.status_code == 200
    assert resolve_res.json()["is_resolved"] is True
