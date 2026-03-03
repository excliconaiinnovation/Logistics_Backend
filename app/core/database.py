from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# ✅ Async engine
engine = create_async_engine(
    settings.DATABASE_URL,  # e.g., "postgresql+asyncpg://user:pass@localhost/dbname"
    echo=True
)

# ✅ Async session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# ✅ Declarative base
Base = declarative_base()

# ✅ FastAPI dependency
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session