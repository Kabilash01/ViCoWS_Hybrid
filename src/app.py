from flask import Flask, render_template, send_from_directory
import os
import json

app = Flask(__name__)

STATUS_JSON_PATH = "../output/status.json"
CRASH_FRAME_FOLDER = "../output/crash_frames/"
DEFAULT_FRAME = "no_image.png"

@app.route('/')
def dashboard():
    # Load JSON data
    try:
        with open(STATUS_JSON_PATH, "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"[ERROR] Unable to read status.json: {e}")
        data = {
            "weather": "Unknown",
            "crash_detected": False,
            "vsv": 0,
            "vlv": 0,
            "headway": 0,
            "risk": "Unknown",
            "timestamp": "N/A"
        }

    # Try to find latest crash frame
    try:
        all_files = os.listdir(CRASH_FRAME_FOLDER)
        crash_images = [f for f in all_files if f.endswith(".jpg") or f.endswith(".png")]
        crash_images.sort(key=lambda x: os.path.getmtime(os.path.join(CRASH_FRAME_FOLDER, x)), reverse=True)
        crash_img = crash_images[0] if crash_images else DEFAULT_FRAME
    except Exception as e:
        print(f"[ERROR] Unable to fetch crash frame: {e}")
        crash_img = DEFAULT_FRAME

    return render_template("index.html", data=data, crash_img=crash_img)

@app.route('/crash_frame/<filename>')
def crash_frame(filename):
    return send_from_directory(CRASH_FRAME_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
