from fastapi import APIRouter, HTTPException
from app.models import InvoiceRequest, OrderRequest, PaymentVerificationRequest, PaymentLinkRequest
from app.services.razorpay_service import create_payment_link, create_order, verify_payment

router = APIRouter()

@router.post("/generate-order")
async def generate_order_endpoint(req: OrderRequest):
    res = await create_order(req.amount)
    if "error" in res:
        raise HTTPException(status_code=500, detail=res["error"])
    return res

@router.post("/verify-payment")
async def verify_payment_endpoint(req: PaymentVerificationRequest):
    params = {
        "razorpay_order_id": req.razorpay_order_id,
        "razorpay_payment_id": req.razorpay_payment_id,
        "razorpay_signature": req.razorpay_signature
    }
    if verify_payment(params):
        return {"message": "Payment verified successfully"}
    else:
        raise HTTPException(status_code=400, detail="Payment verification failed")

@router.post("/create-payment-link")
async def create_payment_link_endpoint(req: PaymentLinkRequest):
    customer = {"name": req.name, "email": req.email, "phone": req.contact}
    desc = "Travel booking"
    try:
        res = await create_payment_link(req.amount, customer, desc)
        if "error" in res:
             raise HTTPException(status_code=500, detail=res["error"])
        # The user's example expects {"payment_link": url}
        # The service returns the full razorpay response or mock dict
        url = res.get("short_url")
        return {"payment_link": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-invoice")
async def generate_invoice(req: InvoiceRequest):
    customer = {"name": req.name, "email": req.email, "phone": req.phone}
    desc = f"Booking: {req.package_name}"
    try:
        res = await create_payment_link(req.amount, customer, desc)
        return {"invoice": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
