# app/models/maintenance.py
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.models.base import Base

class Maintenance(Base):
    __tablename__ = "maintenance"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    maintenance_type = Column(String)
    issue = Column(String)
    odometer = Column(Integer)
    parts_changed = Column(String)
    cost = Column(Float)
    payment_mode = Column(String)
    bill_number = Column(String)
    warranty = Column(String)
    service_date = Column(Date)
    next_service_date = Column(Date)
    bill_file = Column(String)
    remarks = Column(Text)

    # ✅ back_populates to match Vehicle
    vehicle = relationship("Vehicle", back_populates="maintenances")