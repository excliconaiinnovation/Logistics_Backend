from sqlalchemy import Column, Integer, String, Boolean, Text, Float
from app.models.base import Base

class Party(Base):
    __tablename__ = "parties"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    type = Column(String, nullable=False)

    contact_person = Column(String)
    phone = Column(String, nullable=False)
    email = Column(String)

    gst = Column(String)
    pan = Column(String)

    credit_limit = Column(Float)
    payment_terms = Column(Integer)

    address = Column(Text)
    city = Column(String)
    state = Column(String)
    pincode = Column(String)

    notes = Column(Text)

    active = Column(Boolean, default=True)