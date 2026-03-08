from pydantic import BaseModel


class LedgerCreate(BaseModel):
    date: str
    description: str
    type: str
    amount: int


class LedgerResponse(BaseModel):
    id: int
    driver_id: int
    date: str
    description: str
    debit: int
    credit: int
    type: str

    class Config:
        from_attributes = True