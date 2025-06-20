import logging
import json
import requests
from django.conf import settings


class SMSService:
    """Service for sending SMS messages"""

    @classmethod
    def send_sms(cls, phone_number: str, message: str) -> bool:
        """Send an SMS to the given phone number"""
        try:
            payload = {
                "header": {
                    "login": settings.SMS_LOGIN,
                    "pwd": settings.SMS_PASSWORD,
                    "CgPN": settings.SMS_SENDER_ID,
                },
                "body": {
                    # Yaxshiroq identifikator uchun random yoki uuid ishlatishingiz mumkin
                    "message_id_in": abs(hash(phone_number)) % 1000000,
                    "CdPN": phone_number,
                    "text": message,
                },
            }

            print("📤 Payload:\n", json.dumps(payload, indent=4))  # DEBUG

            response = requests.post(settings.SMS_API_URL, json=payload)

            print("📥 Response Status:", response.status_code)  # DEBUG
            print("📥 Response Text:", response.text)            # DEBUG

            if response.status_code == 200:
                logging.info(f"✅ SMS sent successfully to {phone_number}")
                return True
            else:
                logging.error(f"❌ Failed to send SMS: {response.text}")
                return False

        except Exception as e:
            logging.exception(f"❌ Exception sending SMS: {str(e)}")
            return False
