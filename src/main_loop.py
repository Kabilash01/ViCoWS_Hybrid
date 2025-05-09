import cv2
import json
import os
import time
from datetime import datetime
import shutil
from object_detection_tensorflow import detect_crash_from_cctv
from velocity_model import predict_velocity
from collision_predictor import predict_risk
from weather_predictor import predict_weather_from_frame
from tph_estimator import estimate_prediction_horizon
from hybrid_alert_manager import alert_user

VIDEO_PATH = "../data/CCTV_videos/test_videos/test (5).mp4"
STATUS_PATH = "../output/status.json"
CRASH_FRAME_PATH = "../output/crash_frames/latest_crash.jpg"
NO_IMAGE_PATH = "../output/crash_frames/no_image.png"
LOOP_DELAY = 5  # seconds

print("🔄 Starting real-time ViCoWS Hybrid monitoring  loop ....\n")

while True:
    try:
        cap = cv2.VideoCapture(VIDEO_PATH)
        ret, first_frame = cap.read()
        cap.release()

        if not ret:
            print("❌ Error: Unable to read video.")
            continue

        detected_weather = predict_weather_from_frame(first_frame)
        print(f"🌦️ Weather: {detected_weather}")

        crash_detected = detect_crash_from_cctv(VIDEO_PATH, overwrite_latest=True)
        print(f"{'🚨 Crash Detected!' if crash_detected else '✅ No crash detected.'}")

        # ⛔ Overwrite image if no crash detected
        if not crash_detected and os.path.exists(NO_IMAGE_PATH):
            shutil.copy(NO_IMAGE_PATH, CRASH_FRAME_PATH)
            print("🖼️ Showing fallback image: no_image.png")

        predicted_vsv = predict_velocity(first_frame)
        tph_value, tph_level = estimate_prediction_horizon(headway, predicted_vsv, vlv)

        headway = 5
        vlv = 67
        risk = predict_risk(headway, predicted_vsv, vlv)
        risk_label = "High Risk" if risk == 1 else "Safe"

        alert_user(crash_detected, risk)

        status = {
            "weather": detected_weather,
            "crash_detected": crash_detected,
            "vsv": float(predicted_vsv),
            "vlv": float(vlv),
            "headway": float(headway),
            "risk": risk_label,
            "tph": tph_value,
            "tph_level": tph_level,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        os.makedirs(os.path.dirname(STATUS_PATH), exist_ok=True)
        with open(STATUS_PATH, "w", encoding="utf-8") as f:
            json.dump(status, f, indent=4)

        print("✅ Status updated. Sleeping...\n")
        time.sleep(LOOP_DELAY)

    except KeyboardInterrupt:
        print("🛑 Loop stopped by user.")
        break
    except Exception as e:
        print(f"⚠️ Error occurred: {e}")
        time.sleep(LOOP_DELAY)
