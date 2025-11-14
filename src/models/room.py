from sqlalchemy import Column, Integer, String, Float, Enum
from models.base import Base
import enum

class RoomStatus(enum.Enum):
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    CLEANING = "cleaning"

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    room_number = Column(String, unique=True, nullable=False)
    type = Column(String, nullable=False)  # Standard, Deluxe
    price_per_night = Column(Float, nullable=False)
    max_occupancy = Column(Integer, nullable=False)
    status = Column(Enum(RoomStatus), default=RoomStatus.AVAILABLE)
    description = Column(String)
    amenities = Column(String)  # "wifi,tv,ac"