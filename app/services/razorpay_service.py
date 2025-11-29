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
        "reference_id": "pkg_"+str(customer.get("email","unknown")),
        "description": description,
        "customer": {
            "name": customer.get("name"),
            "email": customer.get("email"),
            "contact": customer.get("phone"),
        },
        "notify": {"sms": True, "email": True},
        "reminder_enable": True,
    }
    try:
        res = client.invoice.create(data)  # or use payment link API if preferred
        return res
    except Exception as e:
        print(f"Razorpay Error: {e}")
        return {"error": str(e)}
