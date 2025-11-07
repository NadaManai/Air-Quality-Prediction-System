import sys, os
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


def test_predict_endpoint_structure():
    """✅ Test if the prediction endpoint returns valid structure"""
    payload = {
    "year": 2023,
    "month": 7,
    "day": 15,
    "hour": 10,
    "PRES": 1010,
    "DEWP": 15,
    "PM2.5_log": 3.2,
    "O3_log": 2.9,
    "PM10_log": 3.5,
    "WSPM_log": 1.4,
    "NO2_log": 2.3,
    "PM2.5_monthly_sum": 180,
    "PM10_monthly_sum": 250,
    "SO2_monthly_sum": 35,
    "NO2_monthly_sum": 80,
    "CO_monthly_sum": 22,
    "O3_monthly_sum": 110,
    "CO_ratio": 0.8,
    "O3_ratio": 0.6,
    "TEMP_PRES_interaction": 15000,
    "PM10_EMA_24h": 140,
    "SO2_EMA_24h": 30,
    "NO2_EMA_24h": 70,
    "CO_EMA_24h": 15,
    "O3_EMA_24h": 90,
    "wd_sin": 0.5,
    "wd_cos": -0.3,
    "station_Changping": 0,
    "station_Dingling": 0,
    "station_Dongsi": 1,
    "station_Guanyuan": 0,
    "station_Gucheng": 0,
    "station_Huairou": 0,
    "station_Nongzhanguan": 0,
    "station_Shunyi": 0,
    "station_Tiantan": 0,
    "station_Wanliu": 0,
    "station_Wanshouxigong": 0
}

    response = client.post("/predict", json=payload)
    assert response.status_code == 200, f"Failed with {response.text}"

    data = response.json()
    assert "AQI_prediction" in data, "Missing AQI_prediction in response"
    assert isinstance(data["AQI_prediction"], (float, int)), "AQI_prediction must be numeric"


def test_predict_values_range():
    """✅ Test if predicted AQI is within reasonable bounds"""
    payload = {
    "year": 2023,
    "month": 7,
    "day": 15,
    "hour": 10,
    "PRES": 1010,
    "DEWP": 15,
    "PM2.5_log": 3.2,
    "O3_log": 2.9,
    "PM10_log": 3.5,
    "WSPM_log": 1.4,
    "NO2_log": 2.3,
    "PM2.5_monthly_sum": 180,
    "PM10_monthly_sum": 250,
    "SO2_monthly_sum": 35,
    "NO2_monthly_sum": 80,
    "CO_monthly_sum": 22,
    "O3_monthly_sum": 110,
    "CO_ratio": 0.8,
    "O3_ratio": 0.6,
    "TEMP_PRES_interaction": 15000,
    "PM10_EMA_24h": 140,
    "SO2_EMA_24h": 30,
    "NO2_EMA_24h": 70,
    "CO_EMA_24h": 15,
    "O3_EMA_24h": 90,
    "wd_sin": 0.5,
    "wd_cos": -0.3,
    "station_Changping": 0,
    "station_Dingling": 0,
    "station_Dongsi": 1,
    "station_Guanyuan": 0,
    "station_Gucheng": 0,
    "station_Huairou": 0,
    "station_Nongzhanguan": 0,
    "station_Shunyi": 0,
    "station_Tiantan": 0,
    "station_Wanliu": 0,
    "station_Wanshouxigong": 0
}

    response = client.post("/predict", json=payload)
    result = response.json()["AQI_prediction"]

    assert result >= 0, "AQI cannot be negative"
    assert result < 1000, "AQI unusually high, check model output"
