from sqlalchemy.orm import Session
#from services.room_service import add_room
from models.customer import Customer
from services.room_service import add_room, edit_room, delete_room

def admin_add_room(db: Session):
    print("\n=== THÊM PHÒNG MỚI ===")
    room_number = input("Số phòng: ")
    type = input("Loại phòng (Standard/Deluxe): ")
    price = float(input("Giá mỗi đêm: "))
    occupancy = int(input("Số người tối đa: "))
    desc = input("Mô tả: ")
    amenities = input("Tiện ích (cách nhau bằng dấu phẩy): ")
    add_room(db, room_number=room_number, type=type, price_per_night=price,
             max_occupancy=occupancy, description=desc, amenities=amenities)
    print("Thêm phòng thành công!")

def admin_view_customers(db: Session):
    customers = db.query(Customer).all()
    print("\n=== DANH SÁCH KHÁCH HÀNG ===")
    for c in customers:
        print(f"ID: {c.id} | {c.name} | {c.email}")

# Hàm thêm phòng (nhập liệu từ admin)
def admin_add_room(db: Session):
    print("\n--- THÊM PHÒNG MỚI ---")
    room_number = input("Số phòng: ").strip()
    type = input("Loại phòng (Standard/Deluxe): ").strip()
    max_occupancy = int(input("Số người tối đa: "))
    amenities = input("Tiện ích (cách nhau bằng dấu phẩy): ").strip()
    price_per_night = float(input("Giá mỗi đêm: "))
    description = input("Mô tả (tùy chọn): ").strip()

    try:
        new_room = add_room(
            db=db,
            room_number=room_number,
            type=type,
            max_occupancy=max_occupancy,
            amenities=amenities,
            price_per_night=price_per_night,
            description=description
        )
        print(f"Thêm phòng {new_room.room_number} thành công!")
    except ValueError as e:
        print(f"Lỗi: {e}")

# Hàm chỉnh sửa phòng (nhập liệu từ admin)
def admin_edit_room(db: Session):
    print("\n--- CHỈNH SỬA PHÒNG ---")
    room_id = int(input("ID phòng cần sửa: "))

    type = input("Loại phòng mới (nhấn Enter để bỏ qua): ").strip() or None
    max_occupancy = input("Số người tối đa mới (nhấn Enter để bỏ qua): ").strip()
    max_occupancy = int(max_occupancy) if max_occupancy else None
    amenities = input("Tiện ích mới (nhấn Enter để bỏ qua): ").strip() or None
    price_per_night = input("Giá mỗi đêm mới (nhấn Enter để bỏ qua): ").strip()
    price_per_night = float(price_per_night) if price_per_night else None
    description = input("Mô tả mới (nhấn Enter để bỏ qua): ").strip() or None

    try:
        updated_room = edit_room(
            db=db,
            room_id=room_id,
            type=type,
            max_occupancy=max_occupancy,
            amenities=amenities,
            price_per_night=price_per_night,
            description=description
        )
        print(f"Chỉnh sửa phòng {updated_room.room_number} thành công!")
    except ValueError as e:
        print(f"Lỗi: {e}")

# Hàm xóa phòng (nhập liệu từ admin)
def admin_delete_room(db: Session):
    print("\n--- XÓA PHÒNG ---")
    room_id = int(input("ID phòng cần xóa: "))

    try:
        if delete_room(db, room_id):
            print(f"Xóa phòng ID {room_id} thành công!")
    except ValueError as e:
        print(f"Lỗi: {e}")