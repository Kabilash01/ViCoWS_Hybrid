#test for the continous loop 
TEST_MODE = True

import cv2
import json
import os
from datetime import datetime
import time()
from object_detection_tensorflow import detect_crash_from_cctv
from velocity_model import predict_velocity
from collision_predictor import predict_risk
from weather_predictor import predict_weather_from_frame
from hybrid_alert_manager import alert_user


# -----------------------------
# Step 0: Input Configuration
if TEST_MODE:
    video_path = "../data/CCTV_videos/test_videos/test (4).mp4"
else:
    video_path = 0  # Use webcam (or your Pi's video stream)

status_output_path = "../output/status.json"

# -----------------------------
# Step 1: Get First Frame for Weather Detection
# -----------------------------
cap = cv2.VideoCapture(video_path)
ret, first_frame = cap.read()
cap.release()

if not ret:
    print("❌ Failed to read from video.")
    first_frame = None

# -----------------------------
# Step 2: Detect Weather Condition
# -----------------------------
if first_frame is not None:
    detected_weather = predict_weather_from_frame(first_frame)
    print(f"🌦️ Detected Weather Condition: {detected_weather}")
else:
    detected_weather = "Unknown"
    print("⚠️ Skipped weather detection.")

# -----------------------------
# Step 3: Crash Detection from CCTV
# -----------------------------
try:
    crash_detected = detect_crash_from_cctv(video_path)
    if crash_detected:
        print("🚨 Crash detected in CCTV footage!")
    else:
        print("✅ No crash detected from CCTV footage.")
except Exception as e:
    print(f"⚠️ Crash detection failed: {e}")
    crash_detected = False

# -----------------------------
# Step 4: Predict Future Velocity (VSV)
# -----------------------------
v1, v2, v3, v4 = 60, 62, 61, 63  # Previous speeds in km/h
predicted_vsv = predict_velocity(v1, v2, v3, v4)
print(f"🔵 Predicted Future Speed (VSV): {predicted_vsv:.2f} km/h")

# -----------------------------
# Step 5: Predict Collision Risk
# -----------------------------
headway_m = 5     # Distance to leading vehicle
vlv = 58          # Leading vehicle velocity
predicted_risk = predict_risk(headway_m, predicted_vsv, vlv)

if predicted_risk == 1:
    print("⚠️ High Collision Risk Detected!")
    risk_label = "High Risk"
else:
    print("✅ Safe Situation Predicted.")
    risk_label = "Safe"

# -----------------------------
# Step 6: Final Alert & Dashboard Update
# -----------------------------
alert_user(crash_detected, predicted_risk)

# Save Status JSON for Flask Dashboard
status = {
    "weather": str(detected_weather),
    "crash_detected": bool(crash_detected),
    "vsv": float(predicted_vsv),
    "vlv": float(vlv),
    "headway": float(headway_m),
    "risk": str(risk_label),
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

os.makedirs(os.path.dirname(status_output_path), exist_ok=True)

with open(status_output_path, "w") as f:
    json.dump(status, f, indent=4)

print("✅ status.json saved for dashboard")

# Optional: Validate the saved JSON
try:
    with open(status_output_path, "r") as f:
        json.load(f)
except Exception as err:
    print(f"❌ Corrupted status.json: {err}")

print("\n🏁 ViCoWS Hybrid System Completed Successfully 🏁\n")
