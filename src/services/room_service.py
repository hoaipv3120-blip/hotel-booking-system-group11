from sqlalchemy.orm import Session
from models.room import Room, RoomStatus
from services.booking_service import is_room_available
from datetime import date
from models.room import Room

def add_room(db: Session, **data):
    room = Room(**data)
    db.add(room)
    db.commit()
    db.refresh(room)
    return room

def search_rooms(db: Session, type=None, price_min=0, price_max=float('inf'), guests=1, check_in: date = None, check_out: date = None):
    query = db.query(Room).filter(
        Room.max_occupancy >= guests,
        Room.price_per_night.between(price_min, price_max)
    )
    if type:
        query = query.filter(Room.type == type)
    rooms = query.all()
    if check_in and check_out:
        return [r for r in rooms if is_room_available(db, r.id, check_in, check_out)]
    return rooms

def get_room_by_number(db: Session, room_number: str) -> Room:
    """Lấy phòng theo số phòng"""
    return db.query(Room).filter(Room.room_number == room_number).first()