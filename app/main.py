from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine
from app.models.base import Base
from app.routes import driver
from app.routes import trip
from app.routes import expense
from app.routes import vehicle
from app.routes import maintenance
from app.routes import party
from app.routes import invoice
from app.routes import auth
from app.routes import reports
from app.routes import company
from app.routes import tyre


app = FastAPI()

# ✅ CORS MUST be immediately after app creation
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(driver.router)
app.include_router(trip.router)
app.include_router(expense.router)
app.include_router(vehicle.router)
app.include_router(maintenance.router)
app.include_router(party.router)
app.include_router(invoice.router)
app.include_router(auth.router)
app.include_router(reports.router, prefix="/reports", tags=["Reports"])
app.include_router(company.router)
app.include_router(tyre.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}