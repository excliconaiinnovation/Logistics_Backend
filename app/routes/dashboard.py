from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.core.database import get_db
from app.models.trip import Trip
from app.models.expense import Expense
from app.models.user import User

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/stats")
async def get_dashboard_stats(db: AsyncSession = Depends(get_db)):
    total_expense = await db.execute(select(func.sum(Expense.amount)))
    total_revenue = await db.execute(select(func.sum(Trip.revenue)))
    active_trips = await db.execute(
        select(func.count()).where(Trip.status == "active")
    )

    expense = total_expense.scalar() or 0
    revenue = total_revenue.scalar() or 0
    profit = revenue - expense

    return {
        "today_expense": expense,
        "active_trips": active_trips.scalar(),
        "total_profit": profit,
        "total_revenue": revenue,
    }


@router.get("/expense-trend")
async def expense_trend(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Expense.date, func.sum(Expense.amount))
        .group_by(Expense.date)
    )

    data = result.all()

    return [
        {"day": str(row[0]), "expense": row[1]}
        for row in data
    ]


@router.get("/vehicle-expense")
async def vehicle_expense(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Expense.vehicle_number, func.sum(Expense.amount))
        .group_by(Expense.vehicle_number)
    )

    data = result.all()

    return [
        {"vehicle": row[0], "expense": row[1]}
        for row in data
    ]