import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    GOOGLE_SHEETS_CREDENTIALS_JSON: str = "google_credentials.json"
    SPREADSHEET_ID: str = ""

    VONAGE_API_KEY: str = ""
    VONAGE_API_SECRET: str = ""
    VONAGE_SMS_NUMBER: str = ""

    RAZORPAY_KEY_ID: str = ""
    RAZORPAY_KEY_SECRET: str = ""

    GEMINI_API_KEY: str = ""

    SECRET_KEY: str = "replace_with_random_string"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()
