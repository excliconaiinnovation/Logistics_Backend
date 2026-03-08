from sqlalchemy import Column, Integer, String, Float, Date
from app.models.base import Base

class Tyre(Base):
    __tablename__ = "tyres"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String)
    brand = Column(String)
    size = Column(String)
    pattern = Column(String)
    purchase_date = Column(Date)
    purchase_cost = Column(Float)
    vendor = Column(String)
    vehicle = Column(String)
    position = Column(String)
    current_km = Column(Integer)
    life_km = Column(Integer)
    status = Column(String)
    notes = Column(String)