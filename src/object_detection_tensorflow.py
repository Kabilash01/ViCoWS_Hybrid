import tensorflow as tf
import cv2
import numpy as np
import os
import pandas as pd
from object_detection.utils import label_map_util

# -----------------------------
# CONFIGURATION
# -----------------------------
PATH_TO_SAVED_MODEL = "../models/inference_graph/saved_model"
LABEL_MAP_PATH = "../models/label_map.pbtxt"
CRASH_OUTPUT_FOLDER = "../output/crash_frames/"
SCORE_THRESHOLD = 0.5  # You can fine-tune this

# -----------------------------
# Load Detection Model
# -----------------------------
print("[INFO] Loading TensorFlow object detection model...")
detect_fn = tf.saved_model.load(PATH_TO_SAVED_MODEL)
print("✅ Detection model loaded successfully.")

# Load Label Map
category_index = label_map_util.create_category_index_from_labelmap(
    LABEL_MAP_PATH, use_display_name=True
)

# -----------------------------
# Main Detection Function
# -----------------------------
def detect_crash_from_cctv(video_path, score_threshold=SCORE_THRESHOLD, overwrite_latest=False):
    print(f"[INFO] Opening video: {video_path}")
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("❌ ERROR: Cannot open video.")
        return False

    os.makedirs(CRASH_OUTPUT_FOLDER, exist_ok=True)
    crash_detected = False
    detection_count = 0
    crash_metadata = []
    frame_idx = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_idx += 1

        image_np = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        input_tensor = tf.convert_to_tensor(image_np)[tf.newaxis, ...]

        detections = detect_fn(input_tensor)
        scores = detections['detection_scores'][0].numpy()
        classes = detections['detection_classes'][0].numpy().astype(np.int64)

        for i in range(len(scores)):
            if scores[i] >= score_threshold:
                class_id = classes[i]
                label = category_index.get(class_id, {"name": "N/A"})["name"]
                label = label.strip().lower().replace("_", " ")  # Normalize label name

                print(f"[DEBUG] Frame {frame_idx}: Detected class_id={class_id}, label='{label}', confidence={scores[i]:.2f}")

                # Robust crash detection match
                if "crash" in label:
                    crash_detected = True
                    detection_count += 1

                    filename = "latest_crash.jpg" if overwrite_latest else f"crash_frame_{frame_idx}.jpg"
                    filepath = os.path.join(CRASH_OUTPUT_FOLDER, filename)
                    cv2.imwrite(filepath, frame)

                    print(f"🚨 Crash detected at frame {frame_idx} (Confidence: {scores[i]:.2f})")
                    print(f"✅ Saved crash frame: {filename}")

                    crash_metadata.append({
                        "frame": frame_idx,
                        "confidence": float(scores[i]),
                        "filename": filename
                    })
                    break  # Only log one crash per frame

    cap.release()

    # Save metadata CSV
    if crash_metadata:
        df = pd.DataFrame(crash_metadata)
        meta_path = os.path.join(CRASH_OUTPUT_FOLDER, "crash_metadata.csv")
        df.to_csv(meta_path, index=False)
        print(f"📁 Crash metadata saved to: {meta_path}")

    if not crash_detected:
        print("✅ No crashes detected in this video.")

    return crash_detected
