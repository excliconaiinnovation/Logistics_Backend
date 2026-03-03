from pydantic import BaseModel
from typing import Optional
from datetime import date

class ExpenseCreate(BaseModel):
    trip_id: int
    vehicle: str
    driver: str
    expense_type: str
    amount: float
    payment_mode: str
    notes: Optional[str]

class ExpenseResponse(ExpenseCreate):
    id: int
    created_at: date

    class Config:
        from_attributes = True