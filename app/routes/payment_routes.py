from fastapi import APIRouter, HTTPException
from app.models import InvoiceRequest
from app.services.razorpay_service import create_payment_link

router = APIRouter()

@router.post("/generate-invoice")
async def generate_invoice(req: InvoiceRequest):
    customer = {"name": req.name, "email": req.email, "phone": req.phone}
    desc = f"Booking: {req.package_name}"
    try:
        res = await create_payment_link(req.amount, customer, desc)
        return {"invoice": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
