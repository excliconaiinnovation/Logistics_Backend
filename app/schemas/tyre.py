from pydantic import BaseModel
from datetime import date
from typing import Optional


class TyreBase(BaseModel):
    code: str
    brand: str
    size: str
    pattern: Optional[str] = None
    purchase_date: Optional[date] = None
    purchase_cost: Optional[float] = None
    vendor: Optional[str] = None
    vehicle: Optional[str] = None
    position: Optional[str] = None
    current_km: Optional[int] = 0
    life_km: Optional[int] = 0
    status: Optional[str] = "active"
    notes: Optional[str] = None


class TyreCreate(TyreBase):
    pass


class TyreResponse(TyreBase):
    id: int

    class Config:
        from_attributes = True