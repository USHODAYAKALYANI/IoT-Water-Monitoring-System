from fastapi import FastAPI
import numpy as np

app = FastAPI()

# Dummy ML model simulation
def dummy_predict(distance, temperature):
    activities = ["no_activity", "shower", "faucet", "toilet", "dishwasher"]
    
    index = int(distance + temperature) % len(activities)
    
    prediction = activities[index]
    confidence = round(np.random.uniform(0.7, 0.95), 2)

    return prediction, confidence


@app.get("/")
def root():
    return {"message": "IoT Water Monitoring Backend Running"}


@app.post("/api/v1/predict")
def predict_water_activity(data: dict):

    distance = data["distance"]
    temperature = data["temperature"]

    prediction, confidence = dummy_predict(distance, temperature)

    return {
        "prediction": prediction,
        "confidence": confidence
    }


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
