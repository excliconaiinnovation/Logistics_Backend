from pydantic import BaseModel
from typing import Optional

class PartyBase(BaseModel):
    name: str
    type: str
    contact_person: Optional[str]
    phone: str
    email: Optional[str]
    gst: Optional[str]
    pan: Optional[str]
    credit_limit: Optional[float]
    payment_terms: Optional[int]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    pincode: Optional[str]
    notes: Optional[str]
    active: Optional[bool] = True


class PartyCreate(PartyBase):
    pass


class PartyResponse(PartyBase):
    id: int

    class Config:
        from_attributes = True