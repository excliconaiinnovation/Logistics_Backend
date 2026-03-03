from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.models.base import Base
import datetime

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)

    trip_id = Column(Integer, ForeignKey("trips.id", ondelete="CASCADE"))
    vehicle = Column(String, nullable=False)
    driver = Column(String, nullable=False)

    expense_type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    payment_mode = Column(String, nullable=False)

    notes = Column(Text)

    created_at = Column(Date, default=datetime.date.today)

    trip = relationship("Trip")