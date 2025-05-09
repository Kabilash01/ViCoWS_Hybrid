# src/weather_predictor.py

import cv2
import numpy as np
import json
from tensorflow.keras.models import load_model

# -------------------------
# Load Model and Mapping
# -------------------------
weather_model = load_model('C:/ViCoWS_Hybrid/models/weather_classifier.h5')

with open('C:/ViCoWS_Hybrid/models/label_mapping.json', 'r') as f:
    label_mapping = json.load(f)

reverse_mapping = {v: k for k, v in label_mapping.items()}

# -------------------------
# Weather Prediction Function
# -------------------------
def predict_weather_from_frame(frame):
    """
    Takes a video frame and predicts the weather condition.
    :param frame: OpenCV image frame
    :return: Weather condition as string (e.g., 'Cloudy', 'Sunny', 'Rainy', 'Foggy')
    """
    resized = cv2.resize(frame, (128, 128))
    normalized = resized / 255.0
    input_data = np.expand_dims(normalized, axis=0)
    
    prediction = weather_model.predict(input_data)
    class_idx = np.argmax(prediction)
    weather = reverse_mapping[class_idx]
    return weather
