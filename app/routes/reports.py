from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.core.database import get_db
from app.models.trip import Trip
from app.models.expense import Expense

router = APIRouter()


# 🔹 Trip Profit Report
@router.get("/trip-profit")
async def trip_profit(db: AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(
            Trip.route,
            Trip.vehicle,
            func.sum(Trip.total_freight_amount).label("revenue"),
            func.coalesce(func.sum(Expense.amount), 0).label("expense")
        )
        .outerjoin(Expense, Expense.trip_id == Trip.id)
        .group_by(Trip.route, Trip.vehicle)
    )

    trips = result.all()

    return [
        {
            "route": t.route,
            "vehicle": t.vehicle,
            "revenue": float(t.revenue),
            "expense": float(t.expense),
            "profit": float(t.revenue - t.expense)
        }
        for t in trips
    ]


# 🔹 Monthly Trends API
@router.get("/monthly-trends")
async def monthly_trends(db: AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(
            func.date_trunc('month', Trip.trip_date).label("month"),
            func.sum(Trip.total_freight_amount).label("revenue")
        )
        .group_by("month")
    )

    data = result.all()

    return [
        {
            "month": d.month.strftime("%b"),
            "revenue": float(d.revenue)
        }
        for d in data
    ]

# 🔹 Vehicle Performance
@router.get("/vehicle-performance")
async def vehicle_performance(db: AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(
            Trip.vehicle,
            func.sum(Trip.total_freight_amount).label("revenue")
        )
        .group_by(Trip.vehicle)
    )

    data = result.all()

    return [
        {
            "vehicle": d.vehicle,
            "revenue": float(d.revenue)
        }
        for d in data
    ]
# 🔹 Profit vs Expense
@router.get("/profit-expense")
async def profit_expense(db: AsyncSession = Depends(get_db)):

    revenue_result = await db.execute(
        select(func.sum(Trip.total_freight_amount))
    )

    expense_result = await db.execute(
        select(func.sum(Expense.amount))
    )

    total_revenue = revenue_result.scalar() or 0
    total_expense = expense_result.scalar() or 0

    return {
        "revenue": float(total_revenue),
        "expense": float(total_expense),
        "profit": float(total_revenue - total_expense)
    }


# 🔹 Business Insights
@router.get("/insights")
async def insights(db: AsyncSession = Depends(get_db)):

    revenue_result = await db.execute(
        select(func.sum(Trip.total_freight_amount))
    )

    expense_result = await db.execute(
        select(func.sum(Expense.amount))
    )

    total_revenue = revenue_result.scalar() or 0
    total_expense = expense_result.scalar() or 0

    profit = total_revenue - total_expense
    margin = (profit / total_revenue * 100) if total_revenue else 0

    return {
        "total_revenue": float(total_revenue),
        "total_expense": float(total_expense),
        "profit_margin": round(margin, 2),
        "suggestion":
            "Expenses are high. Optimize fuel costs."
            if margin < 20
            else "Business performing well."
    }
# 🔹 Export Report
@router.get("/export")
async def export_report(period: str, db: AsyncSession = Depends(get_db)):
    return {"message": f"Export for {period} coming soon"}

@router.get("/driver-performance")
async def driver_performance(db: AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(
            Trip.driver,
            func.count(Trip.id).label("trips"),
            func.sum(Trip.total_freight_amount).label("revenue")
        ).group_by(Trip.driver)
    )

    data = result.all()

    return [
        {
            "driver": d.driver,
            "trips": d.trips,
            "revenue": float(d.revenue or 0)
        }
        for d in data
    ]
    
    
@router.get("/recent-trips")
async def recent_trips(db: AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(
            Trip.route,
            Trip.vehicle,
            Trip.freight_from,
            Trip.total_freight_amount
        )
        .order_by(Trip.id.desc())
        .limit(5)
    )

    trips = result.all()

    return [
        {
            "route": t.route,
            "vehicle": t.vehicle,
            "company": t.freight_from,
            "amount": float(t.total_freight_amount or 0)
        }
        for t in trips
    ]
    
    
    