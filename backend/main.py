from fastapi import FastAPI
import psycopg2
import os
from dotenv import load_dotenv
import numpy as np

# Load environment variables
load_dotenv()

app = FastAPI()

# ---------------------------
# Database Connection
# ---------------------------
def get_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        sslmode=os.getenv("DB_SSLMODE")
    )
    return conn


# ---------------------------
# Dummy ML Prediction
# ---------------------------
def dummy_predict(distance, temperature):
    activities = ["no_activity", "shower", "faucet", "toilet", "dishwasher"]

    index = int(distance + temperature) % len(activities)

    prediction = activities[index]
    confidence = round(np.random.uniform(0.7, 0.95), 2)

    return prediction, confidence


# ---------------------------
# Root API
# ---------------------------
@app.get("/")
def root():
    return {"message": "IoT Water Monitoring Backend Running"}


# ---------------------------
# Prediction API
# ---------------------------
@app.post("/api/v1/predict")
def predict_water_activity(data: dict):

    distance = data["distance"]
    temperature = data["temperature"]

    prediction, confidence = dummy_predict(distance, temperature)

    return {
        "prediction": prediction,
        "confidence": confidence
    }


# ---------------------------
# Model Info API
# ---------------------------
@app.get("/api/v1/model-info")
def model_info():

    return {
        "model_type": "LSTM",
        "version": "1.0",
        "accuracy": 0.85,
        "last_trained": "2026-03-10",
        "classes": [
            "no_activity",
            "shower",
            "faucet",
            "toilet",
            "dishwasher"
        ]
    }


# ---------------------------
# Predictions History API
# ---------------------------
@app.get("/api/v1/predictions-history")
def prediction_history():

    return {
        "history": [
            {
                "distance": 25,
                "temperature": 28,
                "prediction": "shower",
                "confidence": 0.91
            },
            {
                "distance": 30,
                "temperature": 27,
                "prediction": "faucet",
                "confidence": 0.87
            }
        ]
    }

