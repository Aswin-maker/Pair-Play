from pydantic import BaseModel, EmailStr
from typing import Optional

class LeadBase(BaseModel):
    customer_name: str
    email: EmailStr
    phone: str
    selected_package: str

class LeadCreate(LeadBase):
    pass

class OTPRequest(BaseModel):
    phone: str

class OTPVerify(BaseModel):
    phone: str
    otp: str
