import os, shutil
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from datetime import date

from app.core.database import get_db
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleResponse

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])

UPLOAD_DIR = "uploads/vehicles"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def save_file(file: UploadFile | None):
    if not file:
        return None
    path = os.path.join(UPLOAD_DIR, file.filename)
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return path


# =========================
# CREATE VEHICLE (FIXED)
# =========================
@router.post("/", response_model=VehicleResponse)
async def create_vehicle(
    number: str = Form(...),
    model: str = Form(...),
    capacity: Optional[float] = Form(None),
    fuel: Optional[str] = Form(None),
    registration_date: Optional[date] = Form(None),
    rc_number: Optional[str] = Form(None),
    purchase_date: Optional[date] = Form(None),
    purchase_amount: Optional[float] = Form(None),
    insurance_company: Optional[str] = Form(None),
    insurance_expiry: Optional[date] = Form(None),
    status: Optional[str] = Form("active"),

    rc_file: UploadFile = File(None),
    insurance_file: UploadFile = File(None),
    pollution_file: UploadFile = File(None),
    permit_file: UploadFile = File(None),

    db: AsyncSession = Depends(get_db)
):

    # 🔥 DUPLICATE CHECK
    existing = await db.execute(
        select(Vehicle).where(Vehicle.number == number)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Vehicle number already exists"
        )

    vehicle = Vehicle(
        number=number,
        model=model,
        capacity=capacity,
        fuel=fuel,
        registration_date=registration_date,
        rc_number=rc_number,
        purchase_date=purchase_date,
        purchase_amount=purchase_amount,
        insurance_company=insurance_company,
        insurance_expiry=insurance_expiry,
        status=status,
        rc_file=save_file(rc_file),
        insurance_file=save_file(insurance_file),
        pollution_file=save_file(pollution_file),
        permit_file=save_file(permit_file),
    )

    try:
        db.add(vehicle)
        await db.commit()
        await db.refresh(vehicle)
        return vehicle

    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Vehicle number already exists"
        )

# =========================
# GET ALL VEHICLES
# =========================
@router.get("/", response_model=List[VehicleResponse])
async def get_vehicles(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Vehicle))
    return result.scalars().all()


# =========================
# GET SINGLE VEHICLE
# =========================
@router.get("/{vehicle_id}", response_model=VehicleResponse)
async def get_vehicle(vehicle_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Vehicle).where(Vehicle.id == vehicle_id)
    )
    vehicle = result.scalar_one_or_none()

    if not vehicle:
        raise HTTPException(404, "Vehicle not found")

    return vehicle