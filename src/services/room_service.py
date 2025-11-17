from sqlalchemy.orm import Session
from models.room import Room, RoomStatus
from services.booking_service import is_room_available
from datetime import date
from models.room import Room

#def add_room(db: Session, **data):
#    room = Room(**data)
#    db.add(room)
#    db.commit()
#    db.refresh(room)
#    return room

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

# Hàm thêm phòng mới (cho admin)
def add_room(db: Session, room_number: str, type: str, max_occupancy: int, amenities: str, price_per_night: float, description: str = "") -> Room:
    # Kiểm tra số phòng đã tồn tại chưa
    existing_room = db.query(Room).filter(Room.room_number == room_number).first()
    if existing_room:
        raise ValueError(f"Phòng {room_number} đã tồn tại!")

    new_room = Room(
        room_number=room_number,
        type=type,
        max_occupancy=max_occupancy,
        amenities=amenities,
        price_per_night=price_per_night,
        description=description,
        status=RoomStatus.available
    )
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room

# Hàm chỉnh sửa phòng (cho admin)
def edit_room(db: Session, room_id: int, type: str = None, max_occupancy: int = None, amenities: str = None, price_per_night: float = None, description: str = None) -> Room:
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise ValueError("Phòng không tồn tại!")

    if type is not None:
        room.type = type
    if max_occupancy is not None:
        room.max_occupancy = max_occupancy
    if amenities is not None:
        room.amenities = amenities
    if price_per_night is not None:
        room.price_per_night = price_per_night
    if description is not None:
        room.description = description

    db.commit()
    db.refresh(room)
    return room

# Hàm xóa phòng (cho admin, chỉ nếu không có booking)
def delete_room(db: Session, room_id: int) -> bool:
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise ValueError("Phòng không tồn tại!")

    # Kiểm tra nếu có booking liên quan
    bookings = db.query(Booking).filter(Booking.room_id == room_id).first()
    if bookings:
        raise ValueError("Phòng đang có booking, không thể xóa!")

    db.delete(room)
    db.commit()
    return True