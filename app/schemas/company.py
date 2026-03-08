from pydantic import BaseModel, EmailStr
from typing import Optional


# Company Register Schema
class CompanyRegister(BaseModel):
    companyName: str
    ownerName: str
    email: EmailStr
    phone: str
    gst: Optional[str] = None
    address: Optional[str] = None
    password: str
    confirmPassword: str


# Company Update Schema (🔥 ADD THIS)
class CompanyUpdate(BaseModel):

    company_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    gst: Optional[str] = None


# Company Response Schema
class CompanyResponse(BaseModel):
    id: int
    company_name: str
    email: str

    class Config:
        from_attributes = True


# Login Request Schema
class LoginRequest(BaseModel):
    username: str
    password: str
    role: str