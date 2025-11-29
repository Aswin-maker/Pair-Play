from fastapi import APIRouter, HTTPException
from app.models import OTPRequest, OTPVerify
from app.services.sms_service import send_otp, verify_otp
import firebase_admin
from firebase_admin import auth, credentials
import os

router = APIRouter()

# Initialize Firebase Admin
# Check if service account file exists to avoid crash on startup
if os.path.exists("firebase_service_account.json"):
    try:
        cred = credentials.Certificate("firebase_service_account.json")
        firebase_admin.initialize_app(cred)
    except ValueError:
        # App already initialized
        pass
    except Exception as e:
        print(f"Firebase Init Error: {e}")
else:
    print("Warning: firebase_service_account.json not found. Firebase Auth will fail.")

@router.post("/verify-firebase-otp")
async def verify_firebase_otp(id_token: dict):
    # Expecting {"id_token": "..."}
    token = id_token.get("id_token")
    if not token:
        raise HTTPException(status_code=400, detail="Missing id_token")
        
    try:
        # In a real scenario, we verify the token
        # decoded_token = auth.verify_id_token(token)
        # phone = decoded_token['phone_number']
        
        # For testing without a real frontend/token, we might need a mock mode 
        # or we just let it fail if the token is invalid.
        # The user requested: "backend will only verify the token"
        
        if os.path.exists("firebase_service_account.json"):
            decoded_token = auth.verify_id_token(token)
            phone = decoded_token.get('phone_number', 'Unknown')
            return {"verified": True, "phone": phone}
        else:
            # Mock behavior if no firebase setup (for testing flow)
            if token == "TEST_TOKEN_MOCK":
                return {"verified": True, "phone": "+919999999999", "mock_mode": True}
            raise HTTPException(status_code=500, detail="Firebase not configured")
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid token: {str(e)}")

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
