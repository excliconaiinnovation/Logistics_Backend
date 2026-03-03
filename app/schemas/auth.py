from pydantic import BaseModel, EmailStr
from typing import Optional


# ================= REGISTER =================

class CompanyRegisterSchema(BaseModel):
    companyName: str
    ownerName: str
    email: EmailStr
    phone: str
    gst: Optional[str] = None
    address: Optional[str] = None
    password: str
    confirmPassword: str


# ================= LOGIN =================

class LoginRequest(BaseModel):
    username: str
    password: str
    role: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ================= FORGOT PASSWORD =================

class ForgotPassword(BaseModel):
    identifier: str  # email or username


# ================= RESET PASSWORD =================

class ResetPassword(BaseModel):
    token: str
    new_password: str