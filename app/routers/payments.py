from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from app.services.payment import payment_service

router = APIRouter()

class InvoiceRequest(BaseModel):
    customer_name: str
    email: EmailStr
    phone: str
    amount: int
    description: str

@router.post("/generate-invoice")
async def generate_invoice(request: InvoiceRequest):
    """
    Generate a payment link/invoice.
    """
    result = payment_service.create_payment_link(
        amount=request.amount,
        description=request.description,
        customer_name=request.customer_name,
        customer_email=request.email,
        customer_phone=request.phone
    )
    return result
