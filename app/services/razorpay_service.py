import razorpay
from app.config import settings

# Initialize client only if keys are present
if settings.RAZORPAY_KEY_ID and settings.RAZORPAY_KEY_SECRET:
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
else:
    client = None

async def create_payment_link(amount_in_rupees: int, customer: dict, description: str):
    if not client:
        return {"error": "Razorpay keys not configured", "short_url": "http://mock-payment-url"}

    # Razorpay expects amount in paise (for INR)
    data = {
        "amount": amount_in_rupees * 100,
        "currency": "INR",
        "accept_partial": False,
        "customer": {
            "name": customer.get("name"),
            "email": customer.get("email"),
            "contact": customer.get("phone"),
        },
        "description": description,
        "callback_url": "https://yourfrontend.com/payment/success",
        "callback_method": "get",
        "notify": {"sms": True, "email": True},
        "reminder_enable": True,
    }
    try:
        # Use payment_link.create instead of invoice.create
        res = client.payment_link.create(data)
        return res
    except Exception as e:
        print(f"Razorpay Error: {e}")
        return {"error": str(e)}

async def create_order(amount: int):
    if not client:
        return {"error": "Razorpay keys not configured", "order_id": "mock_order_id"}
    try:
        order_data = {
            "amount": amount * 100,  # Convert to paise
            "currency": "INR",
            "payment_capture": 1
        }
        order = client.order.create(order_data)
        return order
    except Exception as e:
        return {"error": str(e)}

def verify_payment(params_dict: dict):
    if not client:
        return True # Mock success
    try:
        client.utility.verify_payment_signature(params_dict)
        return True
    except Exception:
        return False
