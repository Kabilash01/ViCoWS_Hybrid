# /src/collision_predictor.py

from tensorflow.keras.models import load_model
import numpy as np

# Load collision risk model
risk_model = load_model('C:/ViCoWS_Hybrid/models/collision_risk_model.h5', compile=False)

def predict_risk(headway, vsv, vlv):
    input_data = np.array([[headway, vsv, vlv]])
    risk_prob = risk_model.predict(input_data)[0][0]
    risk = 1 if risk_prob > 0.5 else 0
    return risk
