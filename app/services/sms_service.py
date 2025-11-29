import os, random
import vonage
from app.config import settings

# Initialize client only if keys are present to avoid errors during startup if keys are missing
if settings.VONAGE_API_KEY and settings.VONAGE_API_SECRET:
    client = vonage.Client(key=settings.VONAGE_API_KEY, secret=settings.VONAGE_API_SECRET)
    sms = vonage.Sms(client)
else:
    client = None
    sms = None

# In-memory store for demo. Replace by a DB for production.
otp_store = {}

async def send_otp(phone: str) -> int:
    otp = random.randint(100000, 999999)
    text = f"Your TravelBot OTP is {otp}"
    
    if sms:
        try:
            response = sms.send_message({
                "from": settings.VONAGE_SMS_NUMBER,
                "to": phone,
                "text": text
            })
            # Check if response indicates failure
            if response["messages"][0]["status"] != "0":
                print(f"Vonage Error: {response['messages'][0]['error-text']}")
                # Fallback to mock or raise? For now, let's just log and maybe fallback
        except Exception as e:
            print(f"Vonage Exception: {e}")
            # Fallback to mock if Vonage fails
            print(f"Fallback Mock SMS to {phone}: {text}")
    else:
        print(f"Mock SMS to {phone}: {text}")

    otp_store[phone] = otp
    return otp

async def verify_otp(phone: str, otp: int) -> bool:
    real = otp_store.get(phone)
    if real and int(real) == int(otp):
        otp_store.pop(phone, None)
        return True
    return False
