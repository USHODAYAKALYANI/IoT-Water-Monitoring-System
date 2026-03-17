import joblib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

# ==============================
# LOAD MODEL
# ==============================
model = joblib.load("water_model.pkl")

# ==============================
# FASTAPI INIT
# ==============================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================
# REQUEST MODEL
# ==============================
class PredictionInput(BaseModel):
    distance: float
    temperature: float


# ==============================
# HISTORY STORAGE (TEMP)
# ==============================
prediction_history = []


# ==============================
# PREDICTION API (AI MODEL)
# ==============================
@app.post("/api/v1/predict")
def predict(data: PredictionInput):

    # Prepare input
    input_data = [[data.distance, data.temperature]]

    # AI Prediction
    prediction = model.predict(input_data)[0]
    confidence = max(model.predict_proba(input_data)[0])

    # Tank Logic
    tank_height = 100  # cm
    water_level = tank_height - data.distance
    water_level = max(0, water_level)

    volume_liters = water_level * 10

    result = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "distance": data.distance,
        "temperature": data.temperature,
        "prediction": prediction,
        "confidence": round(confidence, 2),
        "water_level": round(water_level, 2),
        "volume_liters": round(volume_liters, 2)
    }

    # Save history
    prediction_history.append(result)

    return result


# ==============================
# HISTORY API
# ==============================
@app.get("/api/v1/history")
def get_history():
    return prediction_history


# ==============================
# AUTO PREDICTION (SIMULATION)
# ==============================
import random

@app.get("/api/v1/auto-predict")
def auto_predict():

    # Simulated sensor data
    distance = random.uniform(20, 70)
    temperature = random.uniform(50, 90)

    input_data = [[distance, temperature]]

    prediction = model.predict(input_data)[0]
    confidence = max(model.predict_proba(input_data)[0])

    tank_height = 100
    water_level = tank_height - distance
    water_level = max(0, water_level)

    volume_liters = water_level * 10

    result = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "distance": round(distance, 2),
        "temperature": round(temperature, 2),
        "prediction": prediction,
        "confidence": round(confidence, 2),
        "water_level": round(water_level, 2),
        "volume_liters": round(volume_liters, 2)
    }

    prediction_history.append(result)

    return result