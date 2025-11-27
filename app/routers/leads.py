from fastapi import APIRouter, HTTPException
from app.models.lead import LeadCreate, OTPRequest, OTPVerify
from app.services.otp import otp_service
from app.services.sheets import sheets_service
from datetime import datetime

router = APIRouter()

SHEET_NAME = "TravelPackages"
LEADS_WORKSHEET = "Leads"

@router.post("/send-otp")
async def send_otp(request: OTPRequest):
    """
    Send OTP to the provided phone number.
    """
    result = otp_service.send_otp(request.phone)
    return result

@router.post("/verify-otp")
async def verify_otp(request: OTPVerify):
    """
    Verify the OTP.
    """
    is_valid = otp_service.verify_otp(request.phone, request.otp)
    if is_valid:
        return {"status": "success", "message": "OTP verified successfully"}
    else:
        raise HTTPException(status_code=400, detail="Invalid OTP")

@router.post("/create-lead")
async def create_lead(lead: LeadCreate):
    """
    Create a new lead and save to Google Sheets.
    """
    # In a real flow, you might want to verify OTP again or check a session token
    # For now, we assume the frontend verifies OTP before calling this
    
    row_data = [
        lead.customer_name,
        lead.email,
        lead.phone,
        lead.selected_package,
        "New", # Status
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ]
    
    success = sheets_service.append_row(SHEET_NAME, row_data, LEADS_WORKSHEET)
    
    if success:
        return {"status": "success", "message": "Lead created successfully"}
    else:
        # Fallback if sheets fails (e.g. no creds)
        print(f"Failed to save lead to sheets: {lead}")
        return {"status": "success", "message": "Lead received (Mock save)"}
