import os
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.driver import Driver

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def save_file(file):
    filename = f"{uuid4()}_{file.filename}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as buffer:
        buffer.write(file.file.read())

    return filename


async def create_driver(db: AsyncSession, data, dlFile, aadharFile):

    dl_filename = save_file(dlFile)
    aadhar_filename = save_file(aadharFile)

    driver = Driver(
        **data.model_dump(),   # ✅ Pydantic v2 safe
        dl_file=dl_filename,
        aadhar_file=aadhar_filename
    )

    db.add(driver)

    await db.commit()         # ✅ MUST await
    await db.refresh(driver)  # ✅ MUST await

    return driver