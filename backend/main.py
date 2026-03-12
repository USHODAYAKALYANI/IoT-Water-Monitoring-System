from fastapi import FastAPI
from tensorflow.keras.models import load_model
import numpy as np
import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI()

# Load ML model
model = load_model("saved_models/best_model.h5")

# -------------------------
# Database Connection
# -------------------------
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


# -------------------------
# Root Endpoint
# -------------------------
@app.get("/")
def root():
    return {"message": "IoT Water Monitoring Backend Running"}


# -------------------------
# Model Info Endpoint
# -------------------------
@app.get("/api/v1/model-info")
def get_model_info():

    return {
        "model_type": "LSTM",
        "version": "1.0",
        "accuracy": 0.90,
        "last_trained": "2026-03-12",
        "classes": [
            "no_activity",
            "shower",
            "faucet",
            "toilet",
            "dishwasher"
        ]
    }


# -------------------------
# Prediction Endpoint
# -------------------------
@app.post("/api/v1/predict")
async def predict_water_activity(data: dict):

    distance = float(data["distance"])
    temperature = float(data["temperature"])

    # Model expects 3D input for LSTM
    input_data = np.array([[[distance, temperature, 0]]])

    prediction = model.predict(input_data)

    predicted_class = int(np.argmax(prediction))
    confidence = float(np.max(prediction))

    activity_classes = [
        "no_activity",
        "shower",
        "faucet",
        "toilet",
        "dishwasher"
    ]

    activity = activity_classes[predicted_class]

    return {
        "prediction": activity,
        "confidence": confidence
    }


# -------------------------
# Predictions History Endpoint
# -------------------------
@app.get("/api/v1/predictions-history")
def get_predictions_history():

    # Dummy history for now
    history = [
        {
            "distance": 22,
            "temperature": 29,
            "prediction": "shower",
            "confidence": 0.91,
            "timestamp": str(datetime.now())
        },
        {
            "distance": 30,
            "temperature": 27,
            "prediction": "faucet",
            "confidence": 0.87,
            "timestamp": str(datetime.now())
        }
    ]

    return {"history": history}

