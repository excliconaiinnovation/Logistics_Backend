from pydantic import BaseModel
from typing import Optional
from datetime import date

class InvoiceBase(BaseModel):
    invoice_number: str
    invoice_date: Optional[date] = None
    due_date: Optional[date] = None

    party_id: Optional[int] = None
    vehicle_number: Optional[str] = None
    trip_id: Optional[int] = None

    route: Optional[str] = None

    amount: float
    cgst: float = 0
    sgst: float = 0
    igst: float = 0
    total_amount: float

    gst_type: Optional[str] = None
    gst_number: Optional[str] = None

    notes: Optional[str] = None


class InvoiceCreate(InvoiceBase):
    pass


class InvoiceResponse(InvoiceBase):
    id: int

class InvoiceBase(BaseModel):
    ...
    status: Optional[str] = "Unpaid"
    class Config:
        from_attributes = True