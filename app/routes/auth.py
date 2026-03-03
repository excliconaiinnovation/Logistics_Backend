from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.company import Company
from app.models.user import User
from app.schemas.company import CompanyRegister, CompanyResponse
from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
    ForgotPassword,
    ResetPassword
)
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_reset_token,
    verify_reset_token,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ================= REGISTER =================

@router.post("/register-company", response_model=CompanyResponse)
async def register_company(
    data: CompanyRegister,
    db: AsyncSession = Depends(get_db)
):
    if data.password != data.confirmPassword:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    password_to_hash = data.password[:72]

    result = await db.execute(
        select(User).where(User.email == data.email)
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_company = Company(
        company_name=data.companyName,
        owner_name=data.ownerName,
        email=data.email,
        phone=data.phone,
        gst=data.gst,
        address=data.address,
    )

    db.add(new_company)
    await db.flush()

    new_user = User(
        company_id=new_company.id,
        name=data.ownerName,
        email=data.email,
        password=hash_password(password_to_hash),
        role="admin",
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_company)

    return new_company


# ================= LOGIN =================

@router.post("/login", response_model=TokenResponse)
async def login(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.email == data.username)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if user.role != data.role:
        raise HTTPException(status_code=403, detail="Role mismatch")

    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({
        "user_id": user.id,
        "company_id": user.company_id,
        "role": user.role,
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# ================= FORGOT PASSWORD =================

from fastapi import BackgroundTasks
from app.utils.email import send_reset_email
from app.core.config import FRONTEND_URL


@router.post("/forgot-password")
async def forgot_password(
    data: ForgotPassword,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.email == data.identifier)
    )
    user = result.scalar_one_or_none()

    # 🔐 Security Best Practice:
    # Don't reveal if user exists
    if user:
        reset_token = create_reset_token(user.email)
        reset_link = f"{FRONTEND_URL}/reset-password/{reset_token}"

        background_tasks.add_task(
            send_reset_email,
            user.email,
            reset_link
        )

    return {
        "message": "If this email exists, a reset link has been sent."
    }


# ================= RESET PASSWORD =================

@router.post("/reset-password")
async def reset_password(
    data: ResetPassword,
    db: AsyncSession = Depends(get_db)
):
    email = verify_reset_token(data.token)

    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    if len(data.new_password) < 6:
        raise HTTPException(status_code=400, detail="Password too short")

    result = await db.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password = hash_password(data.new_password[:72])
    await db.commit()

    return {"message": "Password reset successful"}