from sqlalchemy import Column, Integer, Date, Float, Enum, ForeignKey, String
from models.base import Base
import enum
from datetime import date

class BookingStatus(enum.Enum):
    NEW = "New"
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(Enum(BookingStatus), default=BookingStatus.NEW)
    notes = Column(String)
    cancel_reason = Column(String)