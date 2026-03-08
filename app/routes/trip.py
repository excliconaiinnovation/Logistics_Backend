from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.core.database import get_db
from app.models.trip import Trip
from app.schemas.trip import TripCreate, TripResponse

router = APIRouter(
    prefix="/trips",
    tags=["Trips"]
)

# ✅ CREATE TRIP (ASYNC — VERY IMPORTANT)
@router.post("/", response_model=TripResponse)
async def create_trip(
    trip: TripCreate,
    db: AsyncSession = Depends(get_db)
):
    trip_data = trip.dict(exclude_none=True)

    # Auto calculate freight
    if (
        "total_freight_amount" not in trip_data
        and trip.rate_per_unit
        and trip.total_quantity
    ):
        trip_data["total_freight_amount"] = (
            trip.rate_per_unit * trip.total_quantity
        )

    new_trip = Trip(
        **trip_data,
        lr_number=Trip.generate_lr()
    )

    db.add(new_trip)

    # 🔥 THESE MUST BE AWAITED
    await db.commit()
    await db.refresh(new_trip)

    return new_trip


# ✅ GET ALL TRIPS
@router.get("/", response_model=List[TripResponse])
async def get_trips(db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(Trip))
    trips = result.scalars().all()

    response = []

    for trip in trips:
        trip_dict = trip.__dict__

        trip_dict["vehicle_name"] = trip.vehicle
        trip_dict["driver_name"] = trip.driver

        response.append(trip_dict)

    return response


# ✅ GET SINGLE TRIP
@router.get("/{trip_id}", response_model=TripResponse)
async def get_trip(trip_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Trip).where(Trip.id == trip_id)
    )
    trip = result.scalar_one_or_none()

    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    return trip

# ✅ CLOSE TRIP
# CLOSE TRIP
@router.put("/{trip_id}/close", response_model=TripResponse)
async def close_trip(
    trip_id: int,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Trip).where(Trip.id == trip_id)
    )

    trip = result.scalar_one_or_none()

    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    trip.status = "completed"

    await db.commit()
    await db.refresh(trip)

    return trip