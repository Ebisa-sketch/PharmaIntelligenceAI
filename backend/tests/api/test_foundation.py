import pytest
from fastapi.testclient import TestClient


def test_liveness_health_check(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "timestamp" in data


def test_readiness_health_check(client: TestClient):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["healthy", "degraded"]
    assert "database" in data
    assert "timestamp" in data


def test_login_oauth2_success(client: TestClient):
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


def test_login_oauth2_failure(client: TestClient):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "testadmin@pharmaintelligence.et", "password": "WrongPassword!"},
    )
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]


def test_login_json_success(client: TestClient):
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


def test_get_current_user_me(client: TestClient):
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


def test_get_current_user_unauthorized(client: TestClient):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401


def test_token_refresh(client: TestClient):
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
