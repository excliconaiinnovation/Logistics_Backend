from sqlalchemy import Column, Integer, String
from app.models.base import Base

class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)

    # Basic Info
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False)

    # Personal
    dob = Column(String(20))
    gender = Column(String(20))
    bloodGroup = Column(String(10))

    # Address
    address = Column(String(255))
    city = Column(String(100))
    state = Column(String(100))
    pincode = Column(String(10))

    # Documents
    dl = Column(String(50))
    dl_file = Column(String(255))

    aadhar = Column(String(20))
    aadhar_file = Column(String(255))

    vehicle = Column(String(50))

    # Bank
    bankName = Column(String(100))
    accountNumber = Column(String(50))
    ifsc = Column(String(20))

    # Emergency
    emergencyName = Column(String(100))
    emergencyPhone = Column(String(20))
    relation = Column(String(50))