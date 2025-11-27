import vonage
import random
from app.core.config import settings

class OTPService:
    def __init__(self):
        self.otp_storage = {}  # In-memory storage for demo purposes
        self.client = None
        self.sms = None
        
        if settings.VONAGE_API_KEY and settings.VONAGE_API_SECRET:
            try:
                self.client = vonage.Client(
                    key=settings.VONAGE_API_KEY,
                    secret=settings.VONAGE_API_SECRET
                )
                self.sms = vonage.Sms(self.client)
                print("✅ Vonage Client Initialized")
            except Exception as e:
                print(f"⚠️ Vonage Initialization Failed: {e}")
        else:
            print("⚠️ Vonage Credentials Missing - Using Mock Mode")

    def generate_otp(self) -> str:
        return str(random.randint(100000, 999999))

    def send_otp(self, phone: str) -> str:
        otp = self.generate_otp()
        self.otp_storage[phone] = otp
        
        if self.sms and settings.VONAGE_SMS_NUMBER:
            try:
                print(f"📤 Sending OTP via Vonage to {phone}...")
                response = self.sms.send_message({
                    "from": settings.VONAGE_SMS_NUMBER,
                    "to": phone,
                    "text": f"Your OTP code is {otp}",
                })
                
                if response["messages"][0]["status"] == "0":
                    print("✅ SMS sent successfully")
                else:
                    print(f"❌ SMS failed: {response['messages'][0]['error-text']}")
                    
            except Exception as e:
                print(f"❌ Error sending SMS: {e}")
        else:
            print(f"🔔 [MOCK OTP] To: {phone} | Code: {otp}")
            
        return otp

    def verify_otp(self, phone: str, otp: str) -> bool:
        stored_otp = self.otp_storage.get(phone)
        if stored_otp and stored_otp == otp:
            del self.otp_storage[phone]  # OTP is one-time use
            return True
        return False

otp_service = OTPService()
