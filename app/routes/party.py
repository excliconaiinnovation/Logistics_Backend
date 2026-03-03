from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.party import Party
from app.schemas.party import PartyCreate, PartyResponse
from typing import List

router = APIRouter(
    prefix="/parties",
    tags=["Parties"]
)

# ✅ CREATE PARTY
@router.post("/", response_model=PartyResponse)
async def create_party(party: PartyCreate, db: AsyncSession = Depends(get_db)):

    new_party = Party(**party.dict())

    db.add(new_party)
    await db.commit()
    await db.refresh(new_party)

    return new_party


# ✅ GET ALL PARTIES
@router.get("/", response_model=List[PartyResponse])
async def get_parties(db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(Party))
    parties = result.scalars().all()

    return parties


# ✅ GET SINGLE PARTY
@router.get("/{party_id}", response_model=PartyResponse)
async def get_party(party_id: int, db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(Party).where(Party.id == party_id))
    party = result.scalar_one_or_none()

    if not party:
        raise HTTPException(status_code=404, detail="Party not found")

    return party


# ✅ UPDATE PARTY
@router.put("/{party_id}", response_model=PartyResponse)
async def update_party(party_id: int, party_data: PartyCreate, db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(Party).where(Party.id == party_id))
    party = result.scalar_one_or_none()

    if not party:
        raise HTTPException(status_code=404, detail="Party not found")

    for key, value in party_data.dict().items():
        setattr(party, key, value)

    await db.commit()
    await db.refresh(party)

    return party


# ✅ DELETE PARTY
@router.delete("/{party_id}")
async def delete_party(party_id: int, db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(Party).where(Party.id == party_id))
    party = result.scalar_one_or_none()

    if not party:
        raise HTTPException(status_code=404, detail="Party not found")

    await db.delete(party)
    await db.commit()

    return {"message": "Party deleted successfully"}