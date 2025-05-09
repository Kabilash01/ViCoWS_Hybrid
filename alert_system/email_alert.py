# Placeholder for email_alert.py
# alert_system/email_alert.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os

class EmailAlert:
    def __init__(self, location="Unknown Location", image_path="outputs/crash_frames/latest_crash.jpg"):
        self.location = location
        self.image_path = image_path
        self.sender_email = "YOUR_EMAIL@gmail.com"
        self.sender_password = "YOUR_APP_PASSWORD"
        self.receiver_email = "RECEIVER_EMAIL@gmail.com"

    def send_email(self):
        msg = MIMEMultipart()
        msg['Subject'] = "🚨 Vehicle Crash/Collision Risk Detected!"
        msg['From'] = self.sender_email
        msg['To'] = self.receiver_email

        # Email body
        text = (
            f"⚠️ Emergency Notification!\n\n"
            f"A vehicle crash/collision risk was detected.\n"
            f"Location: {self.location}\n"
            f"Please respond immediately!\n\n"
            f"Attached is the latest visual evidence from the detection system."
        )
        msg.attach(MIMEText(text))

        # Attach image if exists
        if os.path.exists(self.image_path):
            with open(self.image_path, 'rb') as img:
                img_data = img.read()
            image = MIMEImage(img_data, name=os.path.basename(self.image_path))
            msg.attach(image)
        else:
            print("[WARNING] No crash image found to attach!")

        # Connect to Gmail server
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, self.receiver_email, msg.as_string())
            server.quit()
            print("[INFO] Email Alert Sent Successfully!")
        except Exception as e:
            print(f"[ERROR] Failed to send email: {e}")

    def run(self):
        self.send_email()
