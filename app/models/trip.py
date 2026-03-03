from sqlalchemy import Column, Integer, String, Float, Date, Text
from app.models.base import Base
import datetime
import random

class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)

    freight_from = Column(String)
    vehicle = Column(String, nullable=False)
    driver = Column(String)

    trip_date = Column(Date, nullable=False)

    route = Column(String)
    loading_point = Column(String)
    unloading_point = Column(String)
    route_distance = Column(Float)

    billing_type = Column(String)
    rate_per_unit = Column(Float)
    total_quantity = Column(Float)
    total_freight_amount = Column(Float)

    start_kms = Column(Float)
    lr_number = Column(String, unique=True)

    reference_lr_number = Column(String)

    eway_bill_number = Column(String)
    eway_bill_expiry = Column(Date)

    invoice_no = Column(String)
    invoice_value = Column(Float)

    packages = Column(Integer)
    weight = Column(String)

    consignor = Column(String)
    consignee = Column(String)
    material = Column(String)
    unit = Column(String)

    notes = Column(Text)

    created_at = Column(Date, default=datetime.date.today)

    @staticmethod
    def generate_lr():
        return f"LR-{random.randint(10000,99999)}"