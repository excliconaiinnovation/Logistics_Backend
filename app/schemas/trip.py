from pydantic import BaseModel
from typing import Optional
from datetime import date

class TripCreate(BaseModel):
    freight_from: Optional[str]
    vehicle: str
    driver: Optional[str]
    trip_date: date

    route: Optional[str]
    loading_point: Optional[str]
    unloading_point: Optional[str]
    route_distance: Optional[float]

    billing_type: Optional[str]
    rate_per_unit: Optional[float]
    total_quantity: Optional[float]
    total_freight_amount: Optional[float]

    start_kms: Optional[float]
    reference_lr_number: Optional[str]

    eway_bill_number: Optional[str]
    eway_bill_expiry: Optional[date]

    invoice_no: Optional[str]
    invoice_value: Optional[float]

    packages: Optional[int]
    weight: Optional[str]

    consignor: Optional[str]
    consignee: Optional[str]
    material: Optional[str]
    unit: Optional[str]

    notes: Optional[str]

class TripResponse(TripCreate):
    id: int
    lr_number: str

    class Config:
        from_attributes = True