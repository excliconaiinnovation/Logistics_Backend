from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.tyre import Tyre
from app.schemas.tyre import TyreCreate, TyreResponse


router = APIRouter(
    prefix="/tyres",
    tags=["Tyres"]
)


# CREATE TYRE
@router.post("/", response_model=TyreResponse)
async def create_tyre(data: TyreCreate, db: AsyncSession = Depends(get_db)):

    tyre = Tyre(**data.model_dump())

    db.add(tyre)
    await db.commit()
    await db.refresh(tyre)

    return tyre


# GET ALL TYRES
@router.get("/", response_model=list[TyreResponse])
async def get_tyres(db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(Tyre))
    tyres = result.scalars().all()

    return tyres


# GET TYRE BY ID
@router.get("/{tyre_id}", response_model=TyreResponse)
async def get_tyre(tyre_id: int, db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(Tyre).where(Tyre.id == tyre_id))
    tyre = result.scalar_one_or_none()

    if not tyre:
        raise HTTPException(status_code=404, detail="Tyre not found")

    return tyre


# UPDATE TYRE
@router.put("/{tyre_id}", response_model=TyreResponse)
async def update_tyre(
    tyre_id: int,
    data: TyreCreate,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(select(Tyre).where(Tyre.id == tyre_id))
    tyre = result.scalar_one_or_none()

    if not tyre:
        raise HTTPException(status_code=404, detail="Tyre not found")

    for key, value in data.model_dump().items():
        setattr(tyre, key, value)

    await db.commit()
    await db.refresh(tyre)

    return tyre


# DELETE TYRE
@router.delete("/{tyre_id}")
async def delete_tyre(tyre_id: int, db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(Tyre).where(Tyre.id == tyre_id))
    tyre = result.scalar_one_or_none()

    if not tyre:
        raise HTTPException(status_code=404, detail="Tyre not found")

    await db.delete(tyre)
    await db.commit()

    return {"message": "Tyre deleted successfully"}


@router.put("/{tyre_id}/damage")
async def mark_tyre_damaged(tyre_id: int, db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(Tyre).where(Tyre.id == tyre_id))
    tyre = result.scalar_one_or_none()

    if not tyre:
        raise HTTPException(status_code=404, detail="Tyre not found")

    tyre.status = "Damaged"

    await db.commit()
    await db.refresh(tyre)

    return {
        "message": "Tyre marked as damaged",
        "data": tyre
    }