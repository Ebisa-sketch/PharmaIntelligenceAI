import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Configure test environment variables before importing app modules
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["ENVIRONMENT"] = "testing"
os.environ["DEBUG"] = "False"

from app.main import app
from app.database.base import Base
from app.database.session import get_db
from app.core.security import get_password_hash
from app.models import Role, Facility, User, Medicine

TEST_DB_URL = "sqlite:///:memory:"
test_engine = create_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Initializes tables and seeds baseline reference data across all tests."""
    Base.metadata.create_all(bind=test_engine)
    session = TestingSessionLocal()

    # 1. Seed Roles
    admin_role = Role(name="admin", description="Administrator")
    manager_role = Role(name="pharmacy_manager", description="Pharmacy Manager")
    researcher_role = Role(name="researcher", description="Researcher")
    guest_role = Role(name="guest", description="Guest")
    session.add_all([admin_role, manager_role, researcher_role, guest_role])
    session.flush()

    # 2. Seed Facilities
    facility1 = Facility(
        code="ETH-TEST-01",
        name="Tikur Anbessa Specialized Hospital Test",
        facility_type="Specialized Referral Hospital",
        region="Addis Ababa",
        is_active=True,
    )
    session.add(facility1)
    session.flush()

    # 3. Seed Users
    admin_user = User(
        email="testadmin@pharmaintelligence.et",
        full_name="Test Administrator",
        hashed_password=get_password_hash("AdminSecret123!"),
        is_active=True,
        role_id=admin_role.id,
        facility_id=facility1.id,
    )
    manager_user = User(
        email="testmanager@pharmaintelligence.et",
        full_name="Test Pharmacy Manager",
        hashed_password=get_password_hash("ManagerSecret123!"),
        is_active=True,
        role_id=manager_role.id,
        facility_id=facility1.id,
    )
    data_user = User(
        email="dataadmin@pharmaintelligence.et",
        full_name="Data Engineering Admin",
        hashed_password=get_password_hash("DataAdminSecret123!"),
        is_active=True,
        role_id=admin_role.id,
        facility_id=facility1.id,
    )
    session.add_all([admin_user, manager_user, data_user])

    # 4. Seed Medicines
    med1 = Medicine(
        code="MED-AMOX-500",
        name="Amoxicillin 500mg Capsule",
        category="Antibiotics",
        dosage_form="Capsule",
        strength="500mg",
        unit_of_measure="Capsule",
        is_essential=True,
        vital_classification="Essential",
    )
    med2 = Medicine(
        code="MED-PARA-500",
        name="Paracetamol 500mg Tablet",
        category="Analgesics",
        dosage_form="Tablet",
        strength="500mg",
        unit_of_measure="Tablet",
        is_essential=True,
        vital_classification="Essential",
    )
    session.add_all([med1, med2])

    session.commit()
    session.close()

    yield

    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db_session():
    """Provides a transactional database session for a test function."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client():
    """Provides a TestClient using the shared application and database."""
    return TestClient(app)


@pytest.fixture
def admin_token_headers(client: TestClient) -> dict:
    """Provides Authorization headers for the authenticated test administrator."""
    response = client.post(
        "/api/v1/auth/login/json",
        json={"email": "testadmin@pharmaintelligence.et", "password": "AdminSecret123!"},
    )
    token = response.json()["token"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def manager_token_headers(client: TestClient) -> dict:
    """Provides Authorization headers for the facility pharmacy manager."""
    response = client.post(
        "/api/v1/auth/login/json",
        json={"email": "testmanager@pharmaintelligence.et", "password": "ManagerSecret123!"},
    )
    token = response.json()["token"]["access_token"]
    return {"Authorization": f"Bearer {token}"}

