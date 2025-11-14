from sqlalchemy.orm import Session
from models.booking import Booking, BookingStatus
from models.room import Room
from datetime import date

def is_room_available(db: Session, room_id: int, check_in: date, check_out: date) -> bool:
    overlapping = db.query(Booking).filter(
        Booking.room_id == room_id,
        Booking.check_in < check_out,
        Booking.check_out > check_in,
        Booking.status != BookingStatus.CANCELLED
    ).first()
    return overlapping is None

def create_booking(db: Session, customer_id: int, room_id: int, check_in: date, check_out: date, notes: str = ""):
    if not is_room_available(db, room_id, check_in, check_out):
        raise ValueError("Phòng đã được đặt")
    room = db.query(Room).filter(Room.id == room_id).first()
    nights = (check_out - check_in).days
    total = nights * room.price_per_night
    booking = Booking(
        customer_id=customer_id, room_id=room_id,
        check_in=check_in, check_out=check_out,
        total_amount=total, notes=notes
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking