from fastapi import APIRouter, HTTPException
from app.models import OTPRequest, OTPVerify
from app.services.sms_service import send_otp, verify_otp

router = APIRouter()

@router.post("/send-otp")
async def send_otp_endpoint(req: OTPRequest):
    otp = await send_otp(req.phone)
    # In production don't return OTP; here for testing you can return it but comment out in prod
    return {"message": "OTP sent", "otp_for_test": otp}

@router.post("/verify-otp")
async def verify_otp_endpoint(req: OTPVerify):
    ok = await verify_otp(req.phone, req.otp)
    if ok:
        return {"verified": True}
    raise HTTPException(status_code=400, detail="Invalid OTP")
