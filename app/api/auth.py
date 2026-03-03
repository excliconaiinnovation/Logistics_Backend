from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.company import Company

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/company-register")
async def register_company(data: dict, db: AsyncSession = Depends(get_db)):
    company = Company(
        name=data["name"],
        email=data["email"],
        phone=data["phone"]
    )

    db.add(company)
    await db.commit()
    await db.refresh(company)

    return {
        "status": "success",
        "company_id": company.id
    }