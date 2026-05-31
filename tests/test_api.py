
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200

def test_predict():
    response = client.post(
        "/predict",
        json={
            "HR": 120,
            "O2Sat": 95,
            "Temp": 39.5,
            "SBP": 100,
            "MAP": 70,
            "Resp": 30,
            "Age": 65,
            "ICULOS": 10
        },
        headers={"Authorization": "Bearer testtoken"}
    )
    assert response.status_code in [200, 401, 403]
