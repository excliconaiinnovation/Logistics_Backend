from pydantic import BaseModel, EmailStr
from typing import Optional


class CompanyRegister(BaseModel):
    companyName: str
    ownerName: str
    email: EmailStr
    phone: str
    gst: Optional[str] = None
    address: Optional[str] = None
    password: str
    confirmPassword: str


class CompanyResponse(BaseModel):
    id: int
    company_name: str
    email: str

    class Config:
        from_attributes = True
        
        