
# -----------------------------------
# FastAPI API Tests
# -----------------------------------

from fastapi.testclient import TestClient

from app.main import app


# FastAPI Test Client
client = TestClient(app)


# -----------------------------------
# Test Root Endpoint
# -----------------------------------

def test_root():

    response = client.get("/")

    assert response.status_code == 200


# -----------------------------------
# Test Predict Endpoint
# -----------------------------------

def test_predict():

    payload = {
        "heart_rate": 120,
        "temperature": 39.5,
        "respiratory_rate": 30
    }

    response = client.post(
        "/predict",
        json=payload
    )

    assert response.status_code in [200, 401, 403]
