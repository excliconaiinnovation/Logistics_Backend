from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from app.models.base import Base
from datetime import datetime
from sqlalchemy.orm import relationship
class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)

    number = Column(String, unique=True, nullable=False)
    model = Column(String, nullable=False)
    capacity = Column(Float)
    fuel = Column(String)

    registration_date = Column(Date)
    rc_number = Column(String)

    purchase_date = Column(Date)
    purchase_amount = Column(Float)

    insurance_company = Column(String)
    insurance_expiry = Column(Date)

    rc_file = Column(String)
    insurance_file = Column(String)
    pollution_file = Column(String)
    permit_file = Column(String)

    status = Column(String, default="active")
    

    created_at = Column(DateTime, default=datetime.utcnow)
    # ✅ FIXED
    # Add this in your Vehicle class
# ✅ Use string name and back_populates
    maintenances = relationship(
        "Maintenance",
        back_populates="vehicle",
        cascade="all, delete-orphan"
    )