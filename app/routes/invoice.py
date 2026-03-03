from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.models.invoice import Invoice
from app.schemas.invoice import InvoiceCreate, InvoiceResponse

router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"]
)


# ✅ CREATE INVOICE (ASYNC)
@router.post("/", response_model=InvoiceResponse)
async def create_invoice(
    data: InvoiceCreate,
    db: AsyncSession = Depends(get_db)
):

    new_invoice = Invoice(**data.dict())

    db.add(new_invoice)

    await db.commit()            # ✅ await required
    await db.refresh(new_invoice)  # ✅ await required

    return new_invoice


# ✅ GET ALL
@router.get("/", response_model=List[InvoiceResponse])
async def get_invoices(db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(Invoice))
    invoices = result.scalars().all()

    return invoices


# ✅ GET SINGLE
@router.get("/{invoice_id}", response_model=InvoiceResponse)
async def get_invoice(invoice_id: int, db: AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(Invoice).where(Invoice.id == invoice_id)
    )
    invoice = result.scalar_one_or_none()

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    return invoice


# ✅ DELETE
@router.delete("/{invoice_id}")
async def delete_invoice(invoice_id: int, db: AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(Invoice).where(Invoice.id == invoice_id)
    )
    invoice = result.scalar_one_or_none()

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    await db.delete(invoice)
    await db.commit()

    return {"message": "Invoice deleted successfully"}