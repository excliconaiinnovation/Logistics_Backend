from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.schemas.driver import DriverResponse, DriverBase
from app.services.driver_service import create_driver
from app.models.driver import Driver 
from fastapi import HTTPException 
from app.models.ledger import Ledger
from app.models.trip import Trip


router = APIRouter(prefix="/drivers", tags=["Drivers"])


@router.post("/", response_model=DriverResponse)
async def add_driver(
    name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    dob: str = Form(...),
    gender: str = Form(...),
    bloodGroup: str = Form(None),

    address: str = Form(...),
    city: str = Form(...),
    state: str = Form(...),
    pincode: str = Form(...),

    dl: str = Form(...),
    aadhar: str = Form(...),
    vehicle: str = Form(...),

    bankName: str = Form(...),
    accountNumber: str = Form(...),
    ifsc: str = Form(...),

    emergencyName: str = Form(...),
    emergencyPhone: str = Form(...),
    relation: str = Form(...),

    dlFile: UploadFile = File(...),
    aadharFile: UploadFile = File(...),

    db: AsyncSession = Depends(get_db)
):
    data = DriverBase(
        name=name,
        phone=phone,
        email=email,
        dob=dob,
        gender=gender,
        bloodGroup=bloodGroup,
        address=address,
        city=city,
        state=state,
        pincode=pincode,
        dl=dl,
        aadhar=aadhar,
        vehicle=vehicle,
        bankName=bankName,
        accountNumber=accountNumber,
        ifsc=ifsc,
        emergencyName=emergencyName,
        emergencyPhone=emergencyPhone,
        relation=relation,
    )

    return await create_driver(db, data, dlFile, aadharFile)


@router.get("/", response_model=list[DriverResponse])
async def get_all_drivers(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Driver))
    drivers = result.scalars().all()
    return drivers

@router.get("/{driver_id}", response_model=DriverResponse)
async def get_driver_by_id(driver_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Driver).where(Driver.id == driver_id))
    driver = result.scalar_one_or_none()

    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")

    return driver

@router.put("/{driver_id}", response_model=DriverResponse)
async def update_driver(
    driver_id: int,
    data: DriverBase,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Driver).where(Driver.id == driver_id))
    driver = result.scalar_one_or_none()

    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")

    for key, value in data.model_dump().items():
        setattr(driver, key, value)

    await db.commit()
    await db.refresh(driver)

    return driver

@router.delete("/{driver_id}")
async def delete_driver(driver_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Driver).where(Driver.id == driver_id))
    driver = result.scalar_one_or_none()

    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")

    await db.delete(driver)
    await db.commit()

    return {"message": "Driver deleted successfully"}

@router.get("/{driver_id}/ledger")
async def get_driver_ledger(driver_id: int, db: AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(Ledger)
        .where(Ledger.driver_id == driver_id)
        .order_by(Ledger.date.desc())
    )

    ledger = result.scalars().all()

    return ledger

@router.get("/{driver_id}/active-trip")
async def get_active_trip(driver_id: int, db: AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(Trip).where(
            Trip.driver_id == driver_id,
            Trip.status == "active"
        )
    )

    trip = result.scalars().first()

    return trip