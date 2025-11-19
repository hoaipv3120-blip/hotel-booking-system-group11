from sqlalchemy import Column, Integer, String, Float, Enum
from models.base import Base
from enum import StrEnum
from sqlalchemy.orm import relationship

class RoomStatus(StrEnum):
    available = "available"
    booked = "booked"
    maintenance = "maintenance"
class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    room_number = Column(String, unique=True, nullable=False)
    type = Column(String, nullable=False)  # Standard, Deluxe
    price_per_night = Column(Float, nullable=False)
    max_occupancy = Column(Integer, nullable=False)
    status = Column(Enum(RoomStatus), default=RoomStatus.available)
    description = Column(String)
    amenities = Column(String)  # "wifi,tv,ac"
    bookings = relationship("Booking", back_populates="room")