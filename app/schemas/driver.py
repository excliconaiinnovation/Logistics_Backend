from pydantic import BaseModel
from typing import Optional

class DriverBase(BaseModel):
    name: str
    phone: str
    email: str
    dob: str
    gender: str
    bloodGroup: Optional[str]

    address: str
    city: str
    state: str
    pincode: str

    dl: str
    aadhar: str
    vehicle: str

    bankName: str
    accountNumber: str
    ifsc: str

    emergencyName: str
    emergencyPhone: str
    relation: str


class DriverResponse(DriverBase):
    id: int

    class Config:
        orm_mode = True