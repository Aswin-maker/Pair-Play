from pydantic import BaseModel, EmailStr
from typing import Optional

class PackageRequest(BaseModel):
    location: Optional[str] = None
    min_budget: Optional[int] = None
    max_budget: Optional[int] = None
    days: Optional[int] = None

class LeadCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    package_name: str

class OTPRequest(BaseModel):
    phone: str

class OTPVerify(BaseModel):
    phone: str
    otp: int

class InvoiceRequest(BaseModel):
    name: str
    email: EmailStr
    phone: str
    package_name: str
    amount: int   # rupees

class FeedbackRequest(BaseModel):
    email: EmailStr
    package_name: str
    feedback: str
