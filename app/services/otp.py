import random
from app.core.config import settings
from twilio.rest import Client

class OTPService:
    def __init__(self):
        self.client = None
        self.mock_otp_store = {}  # Store OTPs in memory for mock/testing
        self.setup_twilio()

    def setup_twilio(self):
        if settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN:
            try:
                self.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            except Exception as e:
                print(f"Twilio setup failed: {e}")

    def generate_otp(self):
        return str(random.randint(100000, 999999))

    def send_otp(self, phone: str):
        otp = self.generate_otp()
        
        # If Twilio is configured, send via SMS
        if self.client and settings.TWILIO_PHONE_NUMBER:
            try:
                message = self.client.messages.create(
                    body=f"Your Travel Chatbot Verification Code is: {otp}",
                    from_=settings.TWILIO_PHONE_NUMBER,
                    to=phone
                )
                # In a real app, you might want to store this in Redis/DB with expiry
                self.mock_otp_store[phone] = otp
                return {"status": "success", "message": "OTP sent via Twilio", "sid": message.sid}
            except Exception as e:
                print(f"Error sending SMS: {e}")
                # Fallback to mock if SMS fails
        
        # Mock behavior
        self.mock_otp_store[phone] = otp
        print(f"MOCK OTP for {phone}: {otp}")
        return {"status": "success", "message": "OTP sent (Mock)", "mock_otp": otp}

    def verify_otp(self, phone: str, otp: str):
        if phone in self.mock_otp_store:
            if self.mock_otp_store[phone] == otp:
                del self.mock_otp_store[phone]  # OTP used
                return True
        return False

otp_service = OTPService()
