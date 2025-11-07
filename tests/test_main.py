import sys, os
import time
import random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home_endpoint():
    """✅ Test if the API root route works"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Air Quality Prediction API is running!"


def test_health_endpoint():
    """✅ Test if the API health endpoint works"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json().get("status") == "ok"


@pytest.mark.parametrize("year, month, day, hour", [
    (2023, 1, 1, 0),
    (2023, 7, 15, 10),
    (2024, 12, 31, 23)
])
def test_predict_various_dates(year, month, day, hour):
    """✅ Test predictions with different dates"""
    payload = {
        "year": year,
        "month": month,
        "day": day,
        "hour": hour,
        "PRES": random.uniform(980, 1050),
        "DEWP": random.uniform(-5, 30),
        "PM2.5_log": random.uniform(0, 10),
        "O3_log": random.uniform(0, 10),
        "PM10_log": random.uniform(0, 10),
        "WSPM_log": random.uniform(0, 5),
        "NO2_log": random.uniform(0, 10),
        "PM2.5_monthly_sum": random.randint(0, 500),
        "PM10_monthly_sum": random.randint(0, 500),
        "SO2_monthly_sum": random.randint(0, 100),
        "NO2_monthly_sum": random.randint(0, 200),
        "CO_monthly_sum": random.randint(0, 50),
        "O3_monthly_sum": random.randint(0, 300),
        "CO_ratio": random.uniform(0, 1),
        "O3_ratio": random.uniform(0, 1),
        "TEMP_PRES_interaction": random.randint(0, 20000),
        "PM10_EMA_24h": random.randint(0, 200),
        "SO2_EMA_24h": random.randint(0, 50),
        "NO2_EMA_24h": random.randint(0, 100),
        "CO_EMA_24h": random.randint(0, 30),
        "O3_EMA_24h": random.randint(0, 200),
        "wd_sin": random.uniform(-1, 1),
        "wd_cos": random.uniform(-1, 1),
        "station_Changping": 0, "station_Dingling": 0, "station_Dongsi": 1,
        "station_Guanyuan": 0, "station_Gucheng": 0, "station_Huairou": 0,
        "station_Nongzhanguan": 0, "station_Shunyi": 0, "station_Tiantan": 0,
        "station_Wanliu": 0, "station_Wanshouxigong": 0
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "AQI_prediction" in data
    assert isinstance(data["AQI_prediction"], (float, int))
    # Reasonable bounds
    result = data["AQI_prediction"]
    assert 0 <= result < 1000, f"AQI out of range: {result}"


def test_predict_response_time():
    """✅ Test if prediction endpoint responds quickly"""
    payload = {
        "year": 2023, "month": 7, "day": 15, "hour": 10,
        "PRES": 1010, "DEWP": 15, "PM2.5_log": 3.2, "O3_log": 2.9,
        "PM10_log": 3.5, "WSPM_log": 1.4, "NO2_log": 2.3,
        "PM2.5_monthly_sum": 180, "PM10_monthly_sum": 250, "SO2_monthly_sum": 35,
        "NO2_monthly_sum": 80, "CO_monthly_sum": 22, "O3_monthly_sum": 110,
        "CO_ratio": 0.8, "O3_ratio": 0.6, "TEMP_PRES_interaction": 15000,
        "PM10_EMA_24h": 140, "SO2_EMA_24h": 30, "NO2_EMA_24h": 70,
        "CO_EMA_24h": 15, "O3_EMA_24h": 90, "wd_sin": 0.5, "wd_cos": -0.3,
        "station_Changping": 0, "station_Dingling": 0, "station_Dongsi": 1,
        "station_Guanyuan": 0, "station_Gucheng": 0, "station_Huairou": 0,
        "station_Nongzhanguan": 0, "station_Shunyi": 0, "station_Tiantan": 0,
        "station_Wanliu": 0, "station_Wanshouxigong": 0
    }
    start = time.time()
    response = client.post("/predict", json=payload)
    duration = time.time() - start
    assert response.status_code == 200
    assert duration < 1.0, f"Prediction took too long: {duration:.2f}s"
