# -----------------------------------
# Authentication & Authorization Tests
# -----------------------------------

from fastapi.testclient import TestClient

from app.main import app


# FastAPI Test Client
client = TestClient(app)


# -----------------------------------
# Test Missing JWT Token
# -----------------------------------

def test_predict_without_token():

    payload = {
        "heart_rate": 120,
        "temperature": 39.5,
        "respiratory_rate": 30
    }

    response = client.post(
        "/predict",
        json=payload
    )

    # Expected:
    # 401 -> Unauthorized
    # 403 -> Forbidden
    # 503 -> OPA/Auth backend unavailable
    assert response.status_code in [401, 403, 503]


# -----------------------------------
# Test Invalid JWT Token
# -----------------------------------

def test_predict_invalid_token():

    payload = {
        "heart_rate": 120,
        "temperature": 39.5,
        "respiratory_rate": 30
    }

    response = client.post(
        "/predict",

        headers={
            "Authorization": "Bearer invalid_token"
        },

        json=payload
    )

    # Expected:
    # 401 -> Unauthorized
    # 403 -> Forbidden
    # 503 -> OPA/Auth backend unavailable
    assert response.status_code in [401, 403, 503]
