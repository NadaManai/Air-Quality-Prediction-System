from fastapi import FastAPI
import pickle
import numpy as np
import pandas as pd

app = FastAPI(title="Air Quality Prediction API")

# Load the model
with open("models/xgboost_model.pkl", "rb") as f:
    model = pickle.load(f)

@app.get("/")
def home():
    return {"message": "Air Quality Prediction API is running!"}

@app.post("/predict")
def predict(features: dict):
    data = pd.DataFrame([features])
    prediction = model.predict(data)[0]
    return {"AQI_prediction": float(prediction)}
