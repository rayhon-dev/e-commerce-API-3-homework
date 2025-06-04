from common.utils.sms_mailing import SMSService

from config.celery import app


@app.task(name="send_message")
def send_sms(phone: str, text: str):
    print(f"Task: Sending SMS to {phone} with text: {text}")
    SMSService.send_sms(phone_number=phone, message=text)
