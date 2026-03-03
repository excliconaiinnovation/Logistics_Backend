from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, extract
from typing import List

from app.core.database import get_db
from app.models.expense import Expense
from app.models.trip import Trip
from app.schemas.expense import ExpenseCreate, ExpenseResponse

router = APIRouter(prefix="/expenses", tags=["Expenses"])


# =========================
# CREATE EXPENSE
# =========================
@router.post("/", response_model=ExpenseResponse)
async def create_expense(
    expense: ExpenseCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Trip).where(Trip.id == expense.trip_id)
    )
    trip = result.scalar_one_or_none()

    if not trip:
        raise HTTPException(status_code=400, detail="Invalid trip_id")

    new_expense = Expense(**expense.model_dump())

    db.add(new_expense)
    await db.commit()
    await db.refresh(new_expense)

    return new_expense


# =========================
# GET ALL EXPENSES (PAGINATION)
# =========================
@router.get("/", response_model=List[ExpenseResponse])
async def get_expenses(
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100),
    db: AsyncSession = Depends(get_db)
):
    offset = (page - 1) * limit

    result = await db.execute(
        select(Expense)
        .order_by(Expense.created_at.desc())
        .offset(offset)
        .limit(limit)
    )

    return result.scalars().all()


# =========================
# GET EXPENSES BY TRIP
# =========================
@router.get("/trip/{trip_id}", response_model=List[ExpenseResponse])
async def get_trip_expenses(
    trip_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Expense).where(Expense.trip_id == trip_id)
    )

    return result.scalars().all()


# =========================
# UPDATE EXPENSE
# =========================
@router.put("/{expense_id}", response_model=ExpenseResponse)
async def update_expense(
    expense_id: int,
    expense: ExpenseCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Expense).where(Expense.id == expense_id)
    )
    existing = result.scalar_one_or_none()

    if not existing:
        raise HTTPException(status_code=404, detail="Expense not found")

    for key, value in expense.model_dump().items():
        setattr(existing, key, value)

    await db.commit()
    await db.refresh(existing)

    return existing


# =========================
# DELETE EXPENSE
# =========================
@router.delete("/{expense_id}")
async def delete_expense(
    expense_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Expense).where(Expense.id == expense_id)
    )
    expense = result.scalar_one_or_none()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    await db.delete(expense)
    await db.commit()

    return {"message": "Expense deleted successfully"}


# =========================
# OVERALL SUMMARY REPORT
# =========================
@router.get("/report/summary")
async def overall_summary(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(
            func.sum(Expense.amount).label("total"),
            func.count(Expense.id).label("entries")
        )
    )

    data = result.first()

    return {
        "total_expense": data.total or 0,
        "total_entries": data.entries
    }


# =========================
# TRIP WISE REPORT
# =========================
@router.get("/report/trip-wise")
async def trip_wise_report(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(
            Expense.trip_id,
            func.sum(Expense.amount).label("total"),
            func.count(Expense.id).label("entries")
        )
        .group_by(Expense.trip_id)
    )

    return [
        {
            "trip_id": r.trip_id,
            "total_expense": r.total,
            "entries": r.entries
        }
        for r in result.all()
    ]


# =========================
# VEHICLE WISE REPORT
# =========================
@router.get("/report/vehicle-wise")
async def vehicle_wise_report(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(
            Expense.vehicle,
            func.sum(Expense.amount).label("total"),
            func.count(Expense.id).label("entries")
        )
        .group_by(Expense.vehicle)
    )

    return [
        {
            "vehicle": r.vehicle,
            "total_expense": r.total,
            "entries": r.entries
        }
        for r in result.all()
    ]


# =========================
# DRIVER WISE REPORT
# =========================
@router.get("/report/driver-wise")
async def driver_wise_report(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(
            Expense.driver,
            func.sum(Expense.amount).label("total"),
            func.count(Expense.id).label("entries")
        )
        .group_by(Expense.driver)
    )

    return [
        {
            "driver": r.driver,
            "total_expense": r.total,
            "entries": r.entries
        }
        for r in result.all()
    ]


# =========================
# MONTHLY REPORT (YEAR WISE)
# =========================
@router.get("/report/monthly")
async def monthly_report(
    year: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(
            extract("month", Expense.created_at).label("month"),
            func.sum(Expense.amount).label("total")
        )
        .where(extract("year", Expense.created_at) == year)
        .group_by("month")
        .order_by("month")
    )

    return [
        {
            "month": int(r.month),
            "total_expense": r.total
        }
        for r in result.all()
    ]