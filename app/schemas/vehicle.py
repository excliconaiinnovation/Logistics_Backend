from pydantic import BaseModel
from typing import Optional
from datetime import date

class VehicleBase(BaseModel):
    number: str
    model: str
    capacity: Optional[float]
    fuel: Optional[str]

    registration_date: Optional[date]
    rc_number: Optional[str]

    purchase_date: Optional[date]
    purchase_amount: Optional[float]

    insurance_company: Optional[str]
    insurance_expiry: Optional[date]

    status: Optional[str]

class VehicleResponse(VehicleBase):
    id: int
    rc_file: Optional[str]
    insurance_file: Optional[str]
    pollution_file: Optional[str]
    permit_file: Optional[str]

    class Config:
        from_attributes = True