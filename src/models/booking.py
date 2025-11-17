from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from models.base import Base
import enum
from datetime import time
from sqlalchemy.orm import relationship

class BookingStatus(enum.Enum):
    confirmed = "Confirmed"
    cancelled = "cancelled"
class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(Enum(BookingStatus), default=BookingStatus.confirmed, nullable=False)
    notes = Column(String, nullable=True)

    customer = relationship("Customer", back_populates="bookings")
    room = relationship("Room", back_populates="bookings")