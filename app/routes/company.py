from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.company import Company
from app.schemas.company import CompanyUpdate

router = APIRouter(prefix="/company", tags=["Company"])


# GET COMPANY PROFILE

@router.get("/profile")
async def get_company_profile(company_id: int, db: AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(Company).where(Company.id == company_id)
    )

    company = result.scalar_one_or_none()

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    return company


# UPDATE COMPANY PROFILE

@router.put("/profile")
async def update_company_profile(
    company_id: int,
    data: CompanyUpdate,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Company).where(Company.id == company_id)
    )

    company = result.scalar_one_or_none()

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    if data.company_name is not None:
        company.company_name = data.company_name

    if data.phone is not None:
        company.phone = data.phone

    if data.email is not None:
        company.email = data.email

    if data.address is not None:
        company.address = data.address

    if data.gst is not None:
        company.gst = data.gst

    await db.commit()
    await db.refresh(company)

    return company