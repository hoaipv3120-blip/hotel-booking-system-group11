from sqlalchemy.orm import Session
from models.booking import Booking, BookingStatus
from models.room import Room
from datetime import date
from datetime import datetime

def is_room_available(db: Session, room_id: int, check_in: date, check_out: date) -> bool:
    overlapping = db.query(Booking).filter(
        Booking.room_id == room_id,
        Booking.status != BookingStatus.cancelled,
        Booking.check_in < check_out,
        Booking.check_out > check_in
    ).first()
    return overlapping is None

def calculate_total_price(room: Room, check_in: date, check_out: date) -> float:
    nights = (check_out - check_in).days
    return room.price_per_night * nights

def create_booking(
    db: Session,
    customer_id: int,
    room_id: int,
    check_in: date,
    check_out: date,
    notes: str = None
) -> Booking:
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise ValueError("Phòng không tồn tại!")

    if not is_room_available(db, room_id, check_in, check_out):
        raise ValueError("Phòng đã được đặt trong khoảng thời gian này!")

    total = calculate_total_price(room, check_in, check_out)

    booking = Booking(
        customer_id=customer_id,
        room_id=room_id,
        check_in=check_in,
        check_out=check_out,
        total_amount=total,
        notes=notes,
        status=BookingStatus.confirmed
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    print(f"Đặt phòng thành công! Mã: #{booking.id} | Trạng thái: Confirmed")
    return booking

def get_bookings_by_customer(db: Session, customer_id: int):
    return db.query(Booking).filter(Booking.customer_id == customer_id).all()

def cancel_booking(session, booking_id: int):
    booking = session.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise ValueError("Không tìm thấy booking!")
    
    if booking.status == BookingStatus.cancelled:
        raise ValueError("Booking đã bị hủy trước đó!")
    
    booking.status = BookingStatus.cancelled
    session.commit()
    print(f"ĐÃ HỦY booking #{booking_id} thành công!")
    return booking

def get_all_bookings(db: Session):
    return db.query(Booking).order_by(Booking.id.desc()).all()

def edit_booking(db: Session, booking_id: int, check_in: str = None, check_out: str = None, phone: str = None, total_amount: float = None, notes: str = None) -> Booking:
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise ValueError("Booking không tồn tại!")

    if check_in:
        booking.check_in = datetime.strptime(check_in, "%Y-%m-%d").date()
    if check_out:
        booking.check_out = datetime.strptime(check_out, "%Y-%m-%d").date()
    if phone:
        booking.customer.phone = phone  
    if total_amount is not None:
        booking.total_amount = total_amount
    if notes is not None:
        booking.notes = notes

    db.commit()
    db.refresh(booking)
    return booking