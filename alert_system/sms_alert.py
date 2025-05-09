# Placeholder for sms_alert.py
# alert_system/sms_alert.py

import requests

class SmsAlert:
    def __init__(self, location="Unknown Location"):
        self.location = location
        self.message = (
            f"🚨 Emergency Alert!\n"
            f"A possible vehicle crash/collision risk detected.\n"
            f"Location: {self.location}\n"
            f"Please dispatch emergency response immediately."
        )

    def send_sms(self):
        url = "https://www.fast2sms.com/dev/bulkV2"
        
        # ⚠️ Enter your Fast2SMS API key here
        api_key = "YOUR_FAST2SMS_API_KEY"
        
        querystring = {
            "authorization": api_key,
            "message": self.message,
            "language": "english",
            "route": "q",
            "numbers": "MOBILE_NUMBER_1,MOBILE_NUMBER_2"  # Enter numbers separated by commas
        }

        headers = {
            'cache-control': "no-cache"
        }

        try:
            response = requests.request("GET", url, headers=headers, params=querystring)
            print("[INFO] SMS Alert Sent Successfully!")
        except Exception as e:
            print(f"[ERROR] Failed to send SMS alert: {e}")

    def run(self):
        self.send_sms()
