from fastapi import FastAPI
from pydantic import BaseModel
import os

import mlflow
import mlflow.sklearn
import numpy as np


class PatientFeatures(BaseModel):
    age: float
    sex: float
    bmi: float
    bp: float
    s1: float
    s2: float
    s3: float
    s4: float
    s5: float
    s6: float


app = FastAPI()

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:8080")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

MODEL_URI = os.getenv("MODEL_URI", "models:/diabets/1")
_model = None


def get_model():
    global _model
    if _model is None:
        _model = mlflow.sklearn.load_model(MODEL_URI)
    return _model


@app.post("/api/v1/predict")
def predict(features: PatientFeatures):
    model = get_model()
    data = np.array(
        [
            [
                features.age,
                features.sex,
                features.bmi,
                features.bp,
                features.s1,
                features.s2,
                features.s3,
                features.s4,
                features.s5,
                features.s6,
            ]
        ]
    )
    prediction = float(model.predict(data)[0])
    return {"predict": prediction}

