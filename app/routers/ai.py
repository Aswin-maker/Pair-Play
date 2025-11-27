from fastapi import APIRouter
from pydantic import BaseModel, EmailStr
from app.services.ai_service import ai_service
from app.services.sheets import sheets_service
from datetime import datetime

router = APIRouter()

FEEDBACK_WORKSHEET = "Feedback"
SHEET_NAME = "TravelPackages"

class AIRequest(BaseModel):
    query: str
    preferences: dict = {}

class FeedbackCreate(BaseModel):
    email: EmailStr
    package_name: str
    feedback: str

@router.post("/recommend")
async def get_recommendation(request: AIRequest):
    """
    Get AI-based travel recommendations.
    """
    recommendation = ai_service.get_recommendation(request.query, request.preferences)
    return {"recommendation": recommendation}

@router.post("/feedback")
async def submit_feedback(feedback: FeedbackCreate):
    """
    Submit user feedback to Google Sheets.
    """
    row_data = [
        feedback.email,
        feedback.package_name,
        feedback.feedback,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ]
    
    success = sheets_service.append_row(SHEET_NAME, row_data, FEEDBACK_WORKSHEET)
    
    if success:
        return {"status": "success", "message": "Feedback submitted successfully"}
    else:
        return {"status": "success", "message": "Feedback received (Mock save)"}
