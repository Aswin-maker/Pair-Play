import os, random
from app.config import settings

# Lazy, defensive Vonage setup: avoid import-time crashes on server
_vonage_client = None
_vonage_sms = None

def _init_vonage():
    global _vonage_client, _vonage_sms
    if _vonage_sms is not None:
        return
    try:
        import vonage
        # SDKs vary; prefer classic Client/Sms if available
        if hasattr(vonage, "Client") and hasattr(vonage, "Sms") and settings.VONAGE_API_KEY and settings.VONAGE_API_SECRET:
            _vonage_client = vonage.Client(key=settings.VONAGE_API_KEY, secret=settings.VONAGE_API_SECRET)
            _vonage_sms = vonage.Sms(_vonage_client)
        else:
            # Unsupported SDK or missing credentials; keep as mock
            _vonage_client = None
            _vonage_sms = None
    except Exception as e:
        # Import errors or API differences → use mock
        print(f"Vonage init skipped: {e}")
        _vonage_client = None
        _vonage_sms = None

# In-memory store for demo. Replace by a DB for production.
otp_store = {}

async def send_otp(phone: str) -> int:
    otp = random.randint(100000, 999999)
    text = f"Your TravelBot OTP is {otp}"
    
    _init_vonage()
    if _vonage_sms:
        try:
            response = _vonage_sms.send_message({
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
