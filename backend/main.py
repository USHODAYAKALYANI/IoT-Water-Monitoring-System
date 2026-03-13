import random
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

prediction_history = []

class PredictionInput(BaseModel):
    distance: float
    temperature: float


# -----------------------------
# Activity prediction logic
# -----------------------------
def predict_activity(distance, temperature):

    if distance > 90 and temperature < 25:
        activity = "no_activity"

    elif distance < 40 and temperature > 25:
        activity = "shower"

    elif distance < 30:
        activity = "faucet"

    elif distance < 20:
        activity = "toilet"

    else:
        activity = "dishwasher"

    confidence = round(random.uniform(0.85, 0.98), 2)

    return activity, confidence


# -----------------------------
# Manual prediction API
# -----------------------------
@app.post("/api/v1/predict")
def predict(data: PredictionInput):

    prediction, confidence = predict_activity(
        data.distance,
        data.temperature
    )

    record = {
        "distance": data.distance,
        "temperature": data.temperature,
        "prediction": prediction,
        "confidence": confidence,
        "time": datetime.now().strftime("%H:%M:%S")
    }

    prediction_history.append(record)

    return record


# -----------------------------
# Auto sensor + tank calculation
# -----------------------------
@app.get("/api/v1/auto-predict")
def auto_predict():

    distance = round(random.uniform(10, 90), 2)
    temperature = round(random.uniform(20, 35), 2)

    tank_height = 100
    tank_length = 100
    tank_width = 100

    water_level = tank_height - distance

    if water_level < 0:
        water_level = 0

    volume_cm3 = water_level * tank_length * tank_width
    volume_liters = round(volume_cm3 / 1000, 2)

    prediction, confidence = predict_activity(distance, temperature)

    record = {
        "distance": distance,
        "temperature": temperature,
        "water_level": water_level,
        "volume_liters": volume_liters,
        "prediction": prediction,
        "confidence": confidence,
        "time": datetime.now().strftime("%H:%M:%S")
    }

    prediction_history.append(record)

    return record


# -----------------------------
# Prediction history
# -----------------------------
@app.get("/api/v1/history")
def history():
    return prediction_history


@app.get("/")
def home():
    return {"message": "IoT Water Monitoring Backend Running"}