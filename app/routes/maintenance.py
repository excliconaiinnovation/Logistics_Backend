from fastapi import APIRouter, Depends, Form, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from datetime import date
import os, shutil

from app.core.database import get_db
from app.models.maintenance import Maintenance
from app.schemas.maintenance import MaintenanceResponse

router = APIRouter(prefix="/maintenance", tags=["Maintenance"])

UPLOAD_DIR = "uploads/maintenance"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ==============================
# Utility: Save File
# ==============================
def save_file(file: UploadFile, upload_dir: str) -> str:
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file_path


# ==============================
# CREATE Maintenance
# ==============================
@router.post("/", response_model=MaintenanceResponse)
async def create_maintenance(
    vehicle_id: int = Form(...),
    maintenanceType: Optional[str] = Form(None),
    issue: Optional[str] = Form(None),
    odometer: Optional[int] = Form(None),
    partsChanged: Optional[str] = Form(None),
    cost: Optional[float] = Form(None),
    paymentMode: Optional[str] = Form(None),
    billNumber: Optional[str] = Form(None),
    warranty: Optional[str] = Form(None),
    serviceDate: Optional[str] = Form(None),
    nextServiceDate: Optional[str] = Form(None),
    remarks: Optional[str] = Form(None),
    billFile: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
):

    def parse_date(date_str: Optional[str]) -> Optional[date]:
        if not date_str:
            return None
        return date.fromisoformat(date_str)

    service_date_parsed = parse_date(serviceDate)
    next_service_date_parsed = parse_date(nextServiceDate)

    file_path = save_file(billFile, UPLOAD_DIR) if billFile else None

    maintenance = Maintenance(
        vehicle_id=vehicle_id,
        maintenance_type=maintenanceType,
        issue=issue,
        odometer=odometer,
        parts_changed=partsChanged,
        cost=cost,
        payment_mode=paymentMode,
        bill_number=billNumber,
        warranty=warranty,
        service_date=service_date_parsed,
        next_service_date=next_service_date_parsed,
        bill_file=file_path,
        remarks=remarks,
    )

    db.add(maintenance)
    await db.flush()
    await db.refresh(maintenance)
    await db.commit()

    return maintenance


# ==============================
# GET All Maintenance
# ==============================
@router.get("/", response_model=List[MaintenanceResponse])
async def get_all_maintenance(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Maintenance).order_by(Maintenance.id.desc())
    )
    return result.scalars().all()


# ==============================
# GET Maintenance By ID
# ==============================
@router.get("/{maintenance_id}", response_model=MaintenanceResponse)
async def get_maintenance_by_id(
    maintenance_id: int,
    db: AsyncSession = Depends(get_db),
):
    maintenance = await db.get(Maintenance, maintenance_id)

    if not maintenance:
        raise HTTPException(status_code=404, detail="Maintenance not found")

    return maintenance


# ==============================
# GET Maintenance By Vehicle
# ==============================
@router.get("/vehicle/{vehicle_id}", response_model=List[MaintenanceResponse])
async def get_maintenance_by_vehicle(
    vehicle_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Maintenance)
        .where(Maintenance.vehicle_id == vehicle_id)
        .order_by(Maintenance.id.desc())
    )
    return result.scalars().all()


# ==============================
# UPDATE Maintenance
# ==============================
@router.put("/{maintenance_id}", response_model=MaintenanceResponse)
async def update_maintenance(
    maintenance_id: int,
    vehicle_id: int = Form(...),
    maintenanceType: Optional[str] = Form(None),
    issue: Optional[str] = Form(None),
    odometer: Optional[int] = Form(None),
    partsChanged: Optional[str] = Form(None),
    cost: Optional[float] = Form(None),
    paymentMode: Optional[str] = Form(None),
    billNumber: Optional[str] = Form(None),
    warranty: Optional[str] = Form(None),
    serviceDate: Optional[str] = Form(None),
    nextServiceDate: Optional[str] = Form(None),
    remarks: Optional[str] = Form(None),
    billFile: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
):

    maintenance = await db.get(Maintenance, maintenance_id)

    if not maintenance:
        raise HTTPException(status_code=404, detail="Maintenance not found")

    maintenance.vehicle_id = vehicle_id
    maintenance.maintenance_type = maintenanceType
    maintenance.issue = issue
    maintenance.odometer = odometer
    maintenance.parts_changed = partsChanged
    maintenance.cost = cost
    maintenance.payment_mode = paymentMode
    maintenance.bill_number = billNumber
    maintenance.warranty = warranty
    maintenance.remarks = remarks

    if serviceDate:
        maintenance.service_date = date.fromisoformat(serviceDate)

    if nextServiceDate:
        maintenance.next_service_date = date.fromisoformat(nextServiceDate)

    if billFile:
        maintenance.bill_file = save_file(billFile, UPLOAD_DIR)

    await db.commit()
    await db.refresh(maintenance)

    return maintenance


# ==============================
# DELETE Maintenance
# ==============================
@router.delete("/{maintenance_id}")
async def delete_maintenance(
    maintenance_id: int,
    db: AsyncSession = Depends(get_db),
):

    maintenance = await db.get(Maintenance, maintenance_id)

    if not maintenance:
        raise HTTPException(status_code=404, detail="Maintenance not found")

    await db.delete(maintenance)
    await db.commit()

    return {"message": "Maintenance deleted successfully"}