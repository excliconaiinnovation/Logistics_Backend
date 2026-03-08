from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.core.database import Base


class Ledger(Base):
    __tablename__ = "ledger"

    id = Column(Integer, primary_key=True, index=True)

    driver_id = Column(Integer, ForeignKey("drivers.id"))

    date = Column(Date)
    description = Column(String)

    debit = Column(Integer, default=0)
    credit = Column(Integer, default=0)

    type = Column(String)  # advance / expense / settlement

    # 🔥 RELATIONSHIP
    driver = relationship("Driver", back_populates="ledger")