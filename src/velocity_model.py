
from tensorflow.keras.models import load_model
import numpy as np

# Load velocity model
velocity_model = load_model('C:/ViCoWS_Hybrid/models/velocity_model.h5', compile=False)

def predict_velocity(v1, v2, v3, v4):
    input_data = np.array([[v1, v2, v3, v4]])
    predicted_vsv = velocity_model.predict(input_data)[0][0]
    return predicted_vsv
