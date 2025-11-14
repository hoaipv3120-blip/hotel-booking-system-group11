from sqlalchemy.orm import Session
from services.room_service import add_room
from models.customer import Customer

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