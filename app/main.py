from fastapi import FastAPI, Response
import pickle
import numpy as np
import pandas as pd
import time
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI(title="Air Quality Prediction API")

@app.get("/health")
def health():
    return {"status": "ok"}

# load the model
with open("Models/xgboost_model.pkl", "rb") as f:
    model = pickle.load(f)

# Prometheus metrics
PREDICTIONS_COUNT = Counter("predictions_total", "Total number of predictions made")
PREDICTION_LATENCY = Histogram("prediction_latency_seconds", "Time taken for predictions")

@app.get("/")
def home():
    return {"message": "Air Quality Prediction API is running!"}

@app.post("/predict")
def predict(features: dict):
    start_time = time.time()
    data = pd.DataFrame([features])
    prediction = model.predict(data)[0]
    duration = time.time() - start_time

    # Update Prometheus metrics
    PREDICTIONS_COUNT.inc()
    PREDICTION_LATENCY.observe(duration)

    return {"AQI_prediction": float(prediction)}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
