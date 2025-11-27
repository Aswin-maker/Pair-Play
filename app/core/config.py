import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Travel Chatbot Backend"
    API_V1_STR: str = "/api/v1"
    
    # Google Sheets
    GOOGLE_SHEETS_CREDENTIALS_JSON: str = os.getenv("GOOGLE_SHEETS_CREDENTIALS_JSON", "")
    
    # Vonage (Nexmo)
    VONAGE_API_KEY: str = os.getenv("VONAGE_API_KEY", "")
    VONAGE_API_SECRET: str = os.getenv("VONAGE_API_SECRET", "")
    VONAGE_SMS_NUMBER: str = os.getenv("VONAGE_SMS_NUMBER", "")
    
    # Razorpay
    RAZORPAY_KEY_ID: str = os.getenv("RAZORPAY_KEY_ID", "")
    RAZORPAY_KEY_SECRET: str = os.getenv("RAZORPAY_KEY_SECRET", "")
    
    # AI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        case_sensitive = True

settings = Settings()
