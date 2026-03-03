from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from app.models.company import Company
from app.models.user import User
from app.schemas.auth import CompanyRegisterSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

async def register_company(db: AsyncSession, data: CompanyRegisterSchema):
    company = Company(
        name=data.companyName,
        gst=data.gst,
        address=data.address
    )
    db.add(company)
    await db.flush()  # company.id available

    admin = User(
        name=data.ownerName,
        email=data.email,
        phone=data.phone,
        password=hash_password(data.password),
        role="admin",
        company_id=company.id
    )

    db.add(admin)
    await db.commit()

    return {
        "message": "Company registered successfully",
        "company_id": company.id
    }