import pytest
from datetime import date, timedelta
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import Facility, Medicine, Inventory, Batch
from app.ml.decensoring import StockoutDecensoringTransformer
from app.ml.syntetos_boylan import SyntetosBoylanClassifier
from app.ml.forecasting import DemandForecaster
from app.ml.stockout_classifier import StockoutRiskClassifier
from app.ml.expiry_simulator import FEFOExpirySimulator
from app.ml.explainability import ExplainabilityEngine
from app.services.forecasting_service import ForecastingService
from app.services.stockout_service import StockoutService
from app.services.expiry_service import ExpiryService


def get_auth_token(client: TestClient) -> str:
    res = client.post(
        "/api/v1/auth/login/json",
        json={"email": "testadmin@pharmaintelligence.et", "password": "AdminSecret123!"},
    )
    return res.json()["token"]["access_token"]


# ──────────────────────────────────────────────────────────────
# 1. Stockout De-censoring Transformer Tests
# ──────────────────────────────────────────────────────────────

def test_decensoring_minor_stockout():
    transformer = StockoutDecensoringTransformer(default_operational_days=30)
    # 2 stockout days (R = 28/30 = 0.933 >= 0.90) -> No adjustment
    res = transformer.decensor_point(observed_consumption=100.0, stockout_days=2)
    assert res["classification"] == "UNCENSORED"
    assert res["adjusted_consumption"] == 100.0
    assert res["in_stock_ratio"] > 0.90


def test_decensoring_moderate_stockout():
    transformer = StockoutDecensoringTransformer(default_operational_days=30)
    # 15 stockout days (R = 15/30 = 0.50) -> Scaled up to 200.0
    res = transformer.decensor_point(observed_consumption=100.0, stockout_days=15)
    assert res["classification"] == "ADJUSTED"
    assert res["adjusted_consumption"] == 200.0


def test_decensoring_true_zero_vs_censored_zero():
    transformer = StockoutDecensoringTransformer(default_operational_days=30)
    # True zero: in-stock > 0, consumption = 0
    res_true = transformer.decensor_point(observed_consumption=0.0, stockout_days=0, closing_stock=50.0)
    assert res_true["classification"] == "TRUE_ZERO"
    assert res_true["adjusted_consumption"] == 0.0

    # Censored zero: closing_stock = 0, stockout_days = 30
    res_cens = transformer.decensor_point(observed_consumption=0.0, stockout_days=30, closing_stock=0.0)
    assert res_cens["classification"] == "CENSORED_ZERO"


def test_decensoring_series_with_imputation():
    transformer = StockoutDecensoringTransformer(default_operational_days=30)
    series = [
        {"observed_consumption": 100.0, "stockout_days": 0},
        {"observed_consumption": 110.0, "stockout_days": 0},
        {"observed_consumption": 0.0, "stockout_days": 30, "closing_stock": 0},  # Severely censored
        {"observed_consumption": 105.0, "stockout_days": 0},
    ]
    transformed = transformer.transform_series(series)
    assert len(transformed) == 4
    assert transformed[2]["classification"] == "IMPUTED"
    assert transformed[2]["adjusted_consumption"] > 0.0


# ──────────────────────────────────────────────────────────────
# 2. Syntetos-Boylan Framework Tests
# ──────────────────────────────────────────────────────────────

def test_syntetos_boylan_classification():
    # Smooth demand: frequent, low variance
    smooth_series = [100.0, 105.0, 95.0, 102.0, 98.0, 104.0]
    res_smooth = SyntetosBoylanClassifier.classify(smooth_series)
    assert res_smooth["category"] == "smooth"
    assert res_smooth["adi"] < 1.32
    assert res_smooth["cv2"] < 0.49

    # Intermittent demand: infrequent with zero periods, low variance when present
    intermittent_series = [0.0, 50.0, 0.0, 0.0, 52.0, 0.0, 48.0, 0.0]
    res_inter = SyntetosBoylanClassifier.classify(intermittent_series)
    assert res_inter["category"] == "intermittent"
    assert res_inter["adi"] >= 1.32
    assert res_inter["recommended_model"] == "croston_sba"


# ──────────────────────────────────────────────────────────────
# 3. Demand Forecaster & Evaluation Metrics Tests
# ──────────────────────────────────────────────────────────────

def test_croston_sba_forecast():
    forecaster = DemandForecaster()
    series = [0.0, 20.0, 0.0, 0.0, 22.0, 0.0]
    forecast = forecaster.croston_sba(series, horizon=3)
    assert len(forecast) == 3
    assert all(val > 0.0 for val in forecast)


def test_multi_model_orchestration_and_metrics():
    forecaster = DemandForecaster()
    series = [100.0, 105.0, 110.0, 108.0, 115.0, 120.0, 118.0, 125.0]

    result = forecaster.forecast(series, horizon=3)
    assert len(result["point_forecasts"]) == 3
    assert result["cumulative_forecast"] > 0.0
    assert result["uncertainty_score"] > 0.0

    # Ensure P10 <= P50 <= P90
    for p10, p50, p90 in zip(result["p10_lower"], result["p50_median"], result["p90_upper"]):
        assert p10 <= p50 <= p90

    # Check metrics
    metrics = result["metrics"]
    assert "rmse" in metrics
    assert "mae" in metrics
    assert "wape" in metrics


# ──────────────────────────────────────────────────────────────
# 4. Stockout Classifier Tests
# ──────────────────────────────────────────────────────────────

def test_stockout_risk_classifier():
    classifier = StockoutRiskClassifier()

    # Critical scenario: Stock exhausted
    crit_pred = classifier.predict_risk(
        facility_id=1,
        facility_name="Tikur Anbessa Hospital",
        medicine_id=1,
        medicine_name="Amoxicillin 500mg",
        usable_stock=0.0,
        daily_consumption=10.0,
        lead_time_days=30.0,
        safety_stock=300.0,
    )
    assert crit_pred["risk_level"] == "Critical"
    assert crit_pred["stockout_risk_score"] == 1.0
    assert crit_pred["days_until_stockout"] == 0.0

    # Safe scenario: Abundant stock
    safe_pred = classifier.predict_risk(
        facility_id=1,
        facility_name="Tikur Anbessa Hospital",
        medicine_id=1,
        medicine_name="Amoxicillin 500mg",
        usable_stock=3000.0,
        daily_consumption=10.0,
        lead_time_days=30.0,
        safety_stock=300.0,
    )
    assert safe_pred["risk_level"] == "Low"
    assert safe_pred["stockout_risk_score"] < 0.30
    assert safe_pred["days_until_stockout"] >= 100.0


# ──────────────────────────────────────────────────────────────
# 5. FEFO Expiry Simulator Tests
# ──────────────────────────────────────────────────────────────

def test_fefo_expiry_simulation():
    simulator = FEFOExpirySimulator(critical_days_threshold=90)
    today = date.today()

    # Daily consumption = 10 units/day
    # Batch 1: 500 units, expires in 30 days -> Demand in 30d = 300 units -> Surplus at risk = 200 units
    batches = [
        {
            "id": 101,
            "batch_number": "BN-SHORT-01",
            "expiry_date": today + timedelta(days=30),
            "quantity_remaining": 500.0,
            "unit_cost_etb": 2.50,
            "status": "Active",
        }
    ]

    sim = simulator.simulate_batches(
        facility_id=1,
        facility_name="Tikur Anbessa",
        medicine_id=1,
        medicine_name="Amoxicillin 500mg",
        batches=batches,
        daily_consumption_rate=10.0,
        today=today,
    )

    assert len(sim) == 1
    record = sim[0]
    assert record["quantity_at_risk"] == pytest.approx(200.0, rel=1e-2)
    assert record["estimated_loss_etb"] == pytest.approx(500.0, rel=1e-2)
    assert record["risk_level"] == "Critical"


# ──────────────────────────────────────────────────────────────
# 6. Explainability Engine Tests
# ──────────────────────────────────────────────────────────────

def test_explainability_forecast_and_stockout():
    # Test forecast explanation
    fc_result = {
        "cumulative_forecast": 360.0,
        "p10_lower": [100.0, 100.0, 100.0],
        "p90_upper": [140.0, 140.0, 140.0],
        "demand_category": "smooth",
        "model_type": "GradientBoostingRegressor",
        "horizon_months": 3,
    }
    explanation = ExplainabilityEngine.explain_forecast(
        medicine_name="Amoxicillin 500mg",
        facility_name="Tikur Anbessa",
        forecast_result=fc_result,
        historical_mean=100.0,
    )
    assert "Over the next 3 months" in explanation["summary"]
    assert len(explanation["feature_attributions"]) >= 1


# ──────────────────────────────────────────────────────────────
# 7. End-to-End API Integration Tests
# ──────────────────────────────────────────────────────────────

def test_api_generate_forecast(client: TestClient, db_session: Session):
    token = get_auth_token(client)

    # Ensure inventory exists for facility 1, medicine 1
    inv = db_session.query(Inventory).filter(Inventory.facility_id == 1, Inventory.medicine_id == 1).first()
    if not inv:
        inv = Inventory(
            facility_id=1,
            medicine_id=1,
            current_stock=1500.0,
            usable_stock=1500.0,
            average_monthly_consumption=500.0,
        )
        db_session.add(inv)
        db_session.commit()

    res = client.post(
        "/api/v1/forecasting/",
        headers={"Authorization": f"Bearer {token}"},
        json={"facility_id": 1, "medicine_id": 1, "horizon_days": 60, "model_type": "ensemble"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["facility_id"] == 1
    assert data["medicine_id"] == 1
    assert data["forecast_value"] > 0
    assert "explanation" in data
    assert len(data["series"]) == 60


def test_api_compare_models(client: TestClient):
    token = get_auth_token(client)
    res = client.get(
        "/api/v1/forecasting/facilities/1/medicines/1/compare",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    data = res.json()
    assert "demand_category" in data
    assert "models_evaluated" in data
    assert "croston_sba" in data["models_evaluated"]


def test_api_stockout_risks(client: TestClient):
    token = get_auth_token(client)
    res = client.get(
        "/api/v1/stockout/facilities/1",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "stockout_risk_score" in data[0]
        assert "risk_level" in data[0]
        assert "explanation" in data[0]


def test_api_expiry_risks(client: TestClient, db_session: Session):
    token = get_auth_token(client)

    # Seed short-dated batch
    batch = Batch(
        facility_id=1,
        medicine_id=1,
        batch_number="TEST-EXPIRY-BATCH-01",
        expiry_date=date.today() + timedelta(days=45),
        quantity_initial=800.0,
        quantity_remaining=800.0,
        unit_cost_etb=2.50,
        status="Active",
    )
    db_session.add(batch)
    db_session.commit()

    res = client.get(
        "/api/v1/expiry/facilities/1",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert any(b["batch_number"] == "TEST-EXPIRY-BATCH-01" for b in data)

