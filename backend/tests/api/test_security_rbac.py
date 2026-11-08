"""
PharmaIntelligence AI - Security & RBAC Integration Tests

Verifies role-based access control, facility multi-tenant isolation,
token security, and authentication boundary defenses.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import create_access_token, get_password_hash
from app.models.user import User
from app.models.role import Role
from app.models.facility import Facility
from app.models.recommendation import RedistributionRecommendation


@pytest.fixture
def security_test_data(db_session: Session):
    """Sets up roles, facilities, and users with distinct privileges."""
    admin_role = db_session.query(Role).filter_by(name="admin").first()
    if not admin_role:
        admin_role = Role(name="admin", description="System Administrator")
        db_session.add(admin_role)

    pharm_role = db_session.query(Role).filter_by(name="pharmacy_manager").first()
    if not pharm_role:
        pharm_role = Role(name="pharmacy_manager", description="Pharmacy Manager")
        db_session.add(pharm_role)

    analyst_role = db_session.query(Role).filter_by(name="data_analyst").first()
    if not analyst_role:
        analyst_role = Role(name="data_analyst", description="Data Analyst")
        db_session.add(analyst_role)

    auditor_role = db_session.query(Role).filter_by(name="auditor").first()
    if not auditor_role:
        auditor_role = Role(name="auditor", description="Auditor")
        db_session.add(auditor_role)

    db_session.flush()

    # Facilities
    fac_1 = db_session.query(Facility).filter_by(code="ETH-TEST-SEC1").first()
    if not fac_1:
        fac_1 = Facility(
            code="ETH-TEST-SEC1",
            name="Security Test Hospital 1",
            facility_type="General Hospital",
            region="Addis Ababa",
            latitude=9.0,
            longitude=38.7,
            storage_capacity_m3=500.0,
            is_active=True,
        )
        db_session.add(fac_1)

    fac_2 = db_session.query(Facility).filter_by(code="ETH-TEST-SEC2").first()
    if not fac_2:
        fac_2 = Facility(
            code="ETH-TEST-SEC2",
            name="Security Test Hospital 2",
            facility_type="General Hospital",
            region="Oromia",
            latitude=8.5,
            longitude=39.2,
            storage_capacity_m3=400.0,
            is_active=True,
        )
        db_session.add(fac_2)

    db_session.flush()

    # Users
    admin_user = db_session.query(User).filter_by(email="sec_admin@sec.et").first()
    if not admin_user:
        admin_user = User(
            email="sec_admin@sec.et",
            full_name="Security Admin",
            hashed_password=get_password_hash("AdminPass123!"),
            is_active=True,
            role_id=admin_role.id,
            facility_id=fac_1.id,
        )
        db_session.add(admin_user)

    manager_1 = db_session.query(User).filter_by(email="mgr_fac1@sec.et").first()
    if not manager_1:
        manager_1 = User(
            email="mgr_fac1@sec.et",
            full_name="Facility 1 Manager",
            hashed_password=get_password_hash("ManagerPass123!"),
            is_active=True,
            role_id=pharm_role.id,
            facility_id=fac_1.id,
        )
        db_session.add(manager_1)

    analyst_user = db_session.query(User).filter_by(email="analyst@sec.et").first()
    if not analyst_user:
        analyst_user = User(
            email="analyst@sec.et",
            full_name="Security Analyst",
            hashed_password=get_password_hash("AnalystPass123!"),
            is_active=True,
            role_id=analyst_role.id,
            facility_id=fac_1.id,
        )
        db_session.add(analyst_user)

    inactive_user = db_session.query(User).filter_by(email="inactive@sec.et").first()
    if not inactive_user:
        inactive_user = User(
            email="inactive@sec.et",
            full_name="Inactive User",
            hashed_password=get_password_hash("InactivePass123!"),
            is_active=False,
            role_id=pharm_role.id,
            facility_id=fac_1.id,
        )
        db_session.add(inactive_user)

    db_session.commit()

    return {
        "admin": admin_user,
        "manager_1": manager_1,
        "analyst": analyst_user,
        "inactive": inactive_user,
        "fac_1": fac_1,
        "fac_2": fac_2,
    }


def test_inactive_user_access_blocked(client: TestClient, security_test_data):
    """Verifies inactive or deactivated accounts cannot authenticate."""
    inactive_user = security_test_data["inactive"]
    token = create_access_token(inactive_user.id)

    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400
    assert "Inactive user account" in response.json()["detail"]


def test_invalid_jwt_token_rejected(client: TestClient):
    """Verifies forged or malformed tokens are rejected with 401 Unauthorized."""
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer completely-bogus-token-string"},
    )
    assert response.status_code == 401
    assert "Could not validate" in response.json()["detail"]


def test_facility_manager_cross_tenant_access_control(client: TestClient, security_test_data):
    """
    Facility multi-tenancy: Pharmacy Manager at Facility 1 must be forbidden
    from accessing stockout risks or inventory at Facility 2.
    """
    manager = security_test_data["manager_1"]
    fac_2 = security_test_data["fac_2"]
    token = create_access_token(manager.id)

    # Attempting to access facility 2 stockout risks
    response = client.get(
        f"/api/v1/stockout/facilities/{fac_2.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403
    assert "Access denied" in response.json()["detail"]


def test_admin_has_cross_facility_access(client: TestClient, security_test_data):
    """System Administrator must have global access to all facilities."""
    admin = security_test_data["admin"]
    fac_2 = security_test_data["fac_2"]
    token = create_access_token(admin.id)

    response = client.get(
        f"/api/v1/stockout/facilities/{fac_2.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200


def test_rbac_redistribution_approval_restricted(client: TestClient, security_test_data, db_session: Session):
    """
    Data Analyst or Auditor role must be forbidden from approving
    redistribution proposals (only admin and pharmacy_manager allowed).
    """
    analyst = security_test_data["analyst"]
    token = create_access_token(analyst.id)

    # Create dummy proposal
    rec = RedistributionRecommendation(
        source_facility_id=security_test_data["fac_1"].id,
        target_facility_id=security_test_data["fac_2"].id,
        medicine_id=1,
        batch_id=None,
        quantity_recommended=50.0,
        status="Pending",
        priority="High",
        transport_distance_km=15.0,
        estimated_transfer_cost_etb=30.0,
        prevented_wastage_cost_etb=500.0,
        rationale="Automated test proposal",
    )
    db_session.add(rec)
    db_session.commit()

    # Analyst tries to approve
    response = client.patch(
        f"/api/v1/redistribution/recommendations/{rec.id}/approve",
        headers={"Authorization": f"Bearer {token}"},
        json={"rationale": "Analyst approval attempt"},
    )
    assert response.status_code == 403
    assert "Operation not permitted" in response.json()["detail"]


def test_sql_injection_resilience_in_parameters(client: TestClient, security_test_data):
    """Verifies that malicious SQL input in query filters does not cause 500 errors."""
    admin = security_test_data["admin"]
    token = create_access_token(admin.id)

    malicious_query = "' OR 1=1; DROP TABLE users; --"
    response = client.get(
        f"/api/v1/inventory/?stock_status={malicious_query}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json() == []
