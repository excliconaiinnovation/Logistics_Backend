from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.models.base import Base

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)

    invoice_number = Column(String, unique=True, nullable=False)
    invoice_date = Column(Date)
    due_date = Column(Date)

    party_id = Column(Integer, ForeignKey("parties.id"))
    vehicle_number = Column(String)
    trip_id = Column(Integer, ForeignKey("trips.id"))

    route = Column(String)

    amount = Column(Float, default=0)
    cgst = Column(Float, default=0)
    sgst = Column(Float, default=0)
    igst = Column(Float, default=0)
    total_amount = Column(Float, default=0)

    gst_type = Column(String)  # with_gst / without_gst
    gst_number = Column(String)

    notes = Column(Text)

    # relationships
    party = relationship("Party")
    trip = relationship("Trip")