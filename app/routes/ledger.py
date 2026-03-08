from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.ledger import Ledger
from app.schemas.ledger import LedgerCreate, LedgerResponse

router = APIRouter(prefix="/ledger", tags=["Ledger"])


@router.get("/{driver_id}", response_model=list[LedgerResponse])
async def get_driver_ledger(driver_id: int, db: AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(Ledger).where(Ledger.driver_id == driver_id)
    )

    return result.scalars().all()


@router.post("/{driver_id}", response_model=LedgerResponse)
async def add_ledger_entry(
    driver_id: int,
    data: LedgerCreate,
    db: AsyncSession = Depends(get_db)
):

    debit = 0
    credit = 0

    if data.type == "advance":
        debit = data.amount
    else:
        credit = data.amount

    entry = Ledger(
        driver_id=driver_id,
        date=data.date,
        description=data.description,
        type=data.type,
        debit=debit,
        credit=credit
    )

    db.add(entry)
    await db.commit()
    await db.refresh(entry)

    return entry

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_db
from app.models.ledger import Ledger

router = APIRouter(prefix="/drivers", tags=["Driver Ledger"])


@router.get("/{driver_id}/ledger")
async def get_driver_ledger(driver_id: int, db: AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(Ledger).where(Ledger.driver_id == driver_id)
    )

    ledger = result.scalars().all()

    return ledger