from fastapi import FastAPI, Request, Response
import pickle
import pandas as pd
import time
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI(title="Air Quality Prediction API")

# -----------------------------
# Load ML model
# -----------------------------
with open("Models/xgboost_model.pkl", "rb") as f:
    model = pickle.load(f)

# -----------------------------
# Prometheus Metrics
# -----------------------------
# Total number of predictions made
PREDICTIONS_COUNT = Counter(
    "predictions_total",
    "Total number of predictions made"
)

# Histogram for prediction latency
PREDICTION_LATENCY = Histogram(
    "prediction_latency_seconds",
    "Time taken for predictions"
)

# Gauge for latest AQI predicted
PREDICTION_VALUE = Gauge(
    "aqi_prediction_value",
    "Latest predicted AQI value"
)

# Total requests per endpoint/method/status
REQUESTS_COUNT = Counter(
    "requests_total",
    "Total API requests",
    ["endpoint", "method", "status"]
)

# Histogram for request latency per endpoint
REQUEST_LATENCY = Histogram(
    "request_latency_seconds",
    "Request latency per endpoint",
    ["endpoint"]
)

# AQI category counters
AQI_HEALTHY = Counter("predictions_healthy", "Predictions with Healthy AQI")
AQI_UNHEALTHY = Counter("predictions_unhealthy", "Predictions with Unhealthy AQI")
AQI_HAZARDOUS = Counter("predictions_hazardous", "Predictions with Hazardous AQI")

# Function to categorize AQI
def aqi_category(aqi):
    if aqi <= 50:
        return "healthy"
    elif aqi <= 100:
        return "unhealthy"
    else:
        return "hazardous"


# -----------------------------
# Health endpoint
# -----------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# -----------------------------
# Home endpoint
# -----------------------------
@app.get("/")
def home():
    return {"message": "Air Quality Prediction API is running!"}

# -----------------------------
# Prediction endpoint
# -----------------------------
@app.post("/predict")
def predict(features: dict, request: Request):
    start_time = time.time()
    try:
        data = pd.DataFrame([features])
        prediction = model.predict(data)[0]
        duration = time.time() - start_time

        # Update metrics
        PREDICTIONS_COUNT.inc()
        PREDICTION_LATENCY.observe(duration)
        PREDICTION_VALUE.set(float(prediction))
        REQUESTS_COUNT.labels(
            endpoint=request.url.path,
            method=request.method,
            status="200"
        ).inc()
        REQUEST_LATENCY.labels(endpoint=request.url.path).observe(duration)

        # Update AQI category counters
        category = aqi_category(prediction)
        if category == "healthy":
            AQI_HEALTHY.inc()
        elif category == "unhealthy":
            AQI_UNHEALTHY.inc()
        else:
            AQI_HAZARDOUS.inc()

        return {"AQI_prediction": float(prediction)}
    
    except Exception as e:
        REQUESTS_COUNT.labels(
            endpoint=request.url.path,
            method=request.method,
            status="500"
        ).inc()
        return {"error": str(e)}


# -----------------------------
# Metrics endpoint for Prometheus
# -----------------------------
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
