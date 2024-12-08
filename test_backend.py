from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_filter_market_data():
    response = client.post(
        "/filter-market-data",
        json={
            "start_date": "2023-01-01",
            "end_date": "2023-01-31",
            "indicators": ["Units Sold"]
        }
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_prediction_chart():
    response = client.get("/predict-trend-chart")
    assert response.status_code == 200
    assert "chart_path" in response.json()
