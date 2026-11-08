import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database.base import Base
from app.database.session import get_db
from app.core.security import get_password_hash
from app.models import Role, Facility, User

# In-memory SQLite engine with StaticPool for isolated multi-connection testing
TEST_DB_URL = "sqlite:///:memory:"
test_engine = create_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=test_engine)
    session = TestingSessionLocal()

    # Seed baseline roles
    admin_role = Role(name="admin", description="Administrator")
    manager_role = Role(name="pharmacy_manager", description="Pharmacy Manager")
    session.add_all([admin_role, manager_role])
    session.flush()

    # Seed test facility
    facility = Facility(
        code="ETH-TEST-01",
        name="Test Referral Hospital",
        facility_type="Specialized Referral Hospital",
        region="Addis Ababa",
        is_active=True,
    )
    session.add(facility)
    session.flush()

    # Seed admin user
    admin_user = User(
        email="testadmin@pharmaintelligence.et",
        full_name="Test Administrator",
        hashed_password=get_password_hash("AdminSecret123!"),
        is_active=True,
        role_id=admin_role.id,
        facility_id=facility.id,
    )
    # Seed manager user
    manager_user = User(
        email="testmanager@pharmaintelligence.et",
        full_name="Test Pharmacy Manager",
        hashed_password=get_password_hash("ManagerSecret123!"),
        is_active=True,
        role_id=manager_role.id,
        facility_id=facility.id,
    )
    session.add_all([admin_user, manager_user])
    session.commit()
    session.close()

    yield

    Base.metadata.drop_all(bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_liveness_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "timestamp" in data


def test_readiness_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["healthy", "degraded"]
    assert "database" in data
    assert "timestamp" in data


def test_login_oauth2_success():
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "testadmin@pharmaintelligence.et", "password": "AdminSecret123!"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["role"] == "admin"
    assert data["user_id"] is not None


def test_login_oauth2_failure():
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "testadmin@pharmaintelligence.et", "password": "WrongPassword!"},
    )
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]


def test_login_json_success():
    response = client.post(
        "/api/v1/auth/login/json",
        json={"email": "testadmin@pharmaintelligence.et", "password": "AdminSecret123!"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert "user" in data
    assert data["user"]["email"] == "testadmin@pharmaintelligence.et"
    assert data["user"]["role"] == "admin"


def test_get_current_user_me():
    # Login first
    login_res = client.post(
        "/api/v1/auth/login/json",
        json={"email": "testadmin@pharmaintelligence.et", "password": "AdminSecret123!"},
    )
    token = login_res.json()["token"]["access_token"]

    # Call /auth/me with Bearer token
    me_res = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_res.status_code == 200
    user_data = me_res.json()
    assert user_data["email"] == "testadmin@pharmaintelligence.et"
    assert user_data["role"] == "admin"


def test_get_current_user_unauthorized():
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401


def test_token_refresh():
    login_res = client.post(
        "/api/v1/auth/login/json",
        json={"email": "testadmin@pharmaintelligence.et", "password": "AdminSecret123!"},
    )
    token = login_res.json()["token"]["access_token"]

    refresh_res = client.post("/api/v1/auth/refresh", json={"token": token})
    assert refresh_res.status_code == 200
    data = refresh_res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

