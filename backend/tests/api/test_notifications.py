from fastapi.testclient import TestClient


def test_notifications_endpoints(client: TestClient, admin_token_headers: dict):
    # 1. Fetch active notifications
    response = client.get("/api/v1/notifications/", headers=admin_token_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

    if len(data) > 0:
        first_id = data[0]["id"]
        # 2. Mark individual notification as read
        read_res = client.post(f"/api/v1/notifications/{first_id}/read", headers=admin_token_headers)
        assert read_res.status_code == 200
        assert read_res.json()["isRead"] is True

    # 3. Mark all as read
    mark_all_res = client.post("/api/v1/notifications/read-all", headers=admin_token_headers)
    assert mark_all_res.status_code == 200
    assert "count" in mark_all_res.json()


def test_experiments_endpoints(client: TestClient, admin_token_headers: dict):
    # 1. List experiments
    res = client.get("/api/v1/experiments/", headers=admin_token_headers)
    assert res.status_code == 200
    assert isinstance(res.json(), list)

    # 2. List model registry
    res_models = client.get("/api/v1/experiments/models", headers=admin_token_headers)
    assert res_models.status_code == 200
    models = res_models.json()
    assert len(models) >= 5

    # 3. Get formal baseline benchmarks
    res_benchmarks = client.get("/api/v1/experiments/benchmarks", headers=admin_token_headers)
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
    res_run = client.post("/api/v1/experiments/run", json=run_payload, headers=admin_token_headers)
    assert res_run.status_code == 200
    run_data = res_run.json()
    assert "experiment_id" in run_data
    assert run_data["status"] == "Completed"

