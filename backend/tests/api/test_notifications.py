from fastapi.testclient import TestClient


def get_auth_headers(client: TestClient) -> dict:
    login_res = client.post(
        "/api/v1/auth/login/json",
        json={"email": "testadmin@pharmaintelligence.et", "password": "AdminSecret123!"},
    )
    assert login_res.status_code == 200
    token = login_res.json()["token"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_notifications_endpoints(client: TestClient):
    headers = get_auth_headers(client)

    # 1. Fetch active notifications
    response = client.get("/api/v1/notifications/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

    if len(data) > 0:
        first_id = data[0]["id"]
        # 2. Mark individual notification as read
        read_res = client.post(f"/api/v1/notifications/{first_id}/read", headers=headers)
        assert read_res.status_code == 200
        assert read_res.json()["isRead"] is True

    # 3. Mark all as read
    mark_all_res = client.post("/api/v1/notifications/read-all", headers=headers)
    assert mark_all_res.status_code == 200
    assert "count" in mark_all_res.json()


def test_experiments_endpoints(client: TestClient):
    headers = get_auth_headers(client)

    # 1. List experiments
    res = client.get("/api/v1/experiments/", headers=headers)
    assert res.status_code == 200
    assert isinstance(res.json(), list)

    # 2. List model registry
    res_models = client.get("/api/v1/experiments/models", headers=headers)
    assert res_models.status_code == 200
    models = res_models.json()
    assert len(models) >= 5

    # 3. Get formal baseline benchmarks
    res_benchmarks = client.get("/api/v1/experiments/benchmarks", headers=headers)
    assert res_benchmarks.status_code == 200
    benchmarks = res_benchmarks.json()
    assert "forecasting" in benchmarks
    assert "stockout_classification" in benchmarks
    assert "expiry_risk" in benchmarks
    assert "redistribution" in benchmarks

    # 4. Trigger reproducible experiment run
    run_payload = {
        "algorithm": "HistGradientBoosting + Croston-SBA Ensemble",
        "split": "80/20 Chronological Split",
        "horizon_days": 90
    }
    res_run = client.post("/api/v1/experiments/run", json=run_payload, headers=headers)
    assert res_run.status_code == 200
    run_data = res_run.json()
    assert "experiment_id" in run_data
    assert run_data["status"] == "Completed"
