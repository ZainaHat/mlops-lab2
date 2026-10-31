import pandas as pd
import pytest
from fastapi.testclient import TestClient

from src.app.main import app

SAMPLE = {
    "tenure_months": 5,
    "monthly_charges": 89.9,
    "contract": "month-to-month",
    "internet_service": "fiber",
    "support_calls": 3,
}


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_model_loads(client):
    model = client.app.state.model
    assert model.classes_.tolist() == [0, 1]
    probabilities = model.predict_proba(pd.DataFrame([SAMPLE]))
    assert probabilities.shape == (1, 2)
    assert probabilities.sum() == pytest.approx(1.0)


def test_prediction_contract(client):
    response = client.post("/predict", json=SAMPLE)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    body = response.json()
    assert set(body) == {"churn_probability"}
    assert isinstance(body["churn_probability"], float)
    assert 0 <= body["churn_probability"] <= 1


def test_missing_field_rejected(client):
    invalid = SAMPLE.copy()
    del invalid["contract"]
    response = client.post("/predict", json=invalid)
    assert response.status_code == 422


@pytest.mark.parametrize(
    "changes",
    [
        {"tenure_months": -1},
        {"monthly_charges": -10},
        {"support_calls": -1},
        {"contract": "invalid"},
        {"internet_service": "invalid"},
        {"unexpected_field": 123},
    ],
)
def test_invalid_input_rejected(client, changes):
    response = client.post("/predict", json={**SAMPLE, **changes})
    assert response.status_code == 422


def test_zero_values_edge_case(client):
    customer = {
        **SAMPLE,
        "tenure_months": 0,
        "monthly_charges": 0,
        "support_calls": 0,
        "internet_service": "none",
    }
    response = client.post("/predict", json=customer)
    assert response.status_code == 200
    assert 0 <= response.json()["churn_probability"] <= 1


def test_deterministic_prediction(client):
    model = client.app.state.model
    expected = round(
        float(model.predict_proba(pd.DataFrame([SAMPLE]))[0, 1]),
        3,
    )
    for _ in range(3):
        response = client.post("/predict", json=SAMPLE)
        assert response.status_code == 200
        assert response.json()["churn_probability"] == expected
