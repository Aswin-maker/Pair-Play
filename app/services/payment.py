import razorpay
from app.core.config import settings
import time

class PaymentService:
    def __init__(self):
        self.client = None
        self.setup_razorpay()

    def setup_razorpay(self):
        if settings.RAZORPAY_KEY_ID and settings.RAZORPAY_KEY_SECRET:
            try:
                self.client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            except Exception as e:
                print(f"Razorpay setup failed: {e}")

    def create_payment_link(self, amount: int, description: str, customer_name: str, customer_email: str, customer_phone: str):
        # Amount in Razorpay is in paise (1 INR = 100 paise)
        amount_paise = amount * 100
        
        if self.client:
            try:
                data = {
                    "amount": amount_paise,
                    "currency": "INR",
                    "accept_partial": False,
                    "description": description,
                    "customer": {
                        "name": customer_name,
                        "email": customer_email,
                        "contact": customer_phone
                    },
                    "notify": {
                        "sms": True,
                        "email": True
                    },
                    "reminder_enable": True,
                    "callback_url": "https://example.com/payment-callback", # Replace with actual callback
                    "callback_method": "get"
                }
                payment_link = self.client.payment_link.create(data)
                return {
                    "status": "success",
                    "payment_link": payment_link.get("short_url"),
                    "id": payment_link.get("id")
                }
            except Exception as e:
                print(f"Error creating Razorpay link: {e}")
                
        # Mock behavior
        mock_link = f"https://rzp.test/pay/{int(time.time())}"
        return {
            "status": "success",
            "message": "Payment link created (Mock)",
            "payment_link": mock_link,
            "amount": amount
        }

payment_service = PaymentService()
