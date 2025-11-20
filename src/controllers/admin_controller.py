from sqlalchemy.orm import Session
from models.customer import Customer
from services.room_service import add_room, edit_room, delete_room
from models.booking import Booking
from services.auth_service import is_admin
from services.booking_service import edit_booking
from models.room import Room, RoomStatus

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

#Hàm xem ds customer
def admin_view_customers(db: Session):
    print("\n" + "="*80)
    print("                DANH SÁCH TẤT CẢ KHÁCH HÀNG")
    print("="*80)
    
    customers = db.query(Customer).all()
    
    if not customers:
        print("  Chưa có khách hàng nào!")
        print("="*80)
        input("\nNhấn Enter để quay lại...")
        return

    for c in customers:
        role = "ADMIN" if is_admin(c) else "KHÁCH HÀNG"
        print(f"  ID: {c.id} | Tên: {c.name} | Email: {c.email}")
        print(f"     Giới tính: {c.gender} | Ngày sinh: {c.dob} | SĐT: {c.phone}")
        print(f"     Địa chỉ: {c.address or 'Không có'} | Vai trò: {role}")
        print("-" * 80)

    input("\nNhấn Enter để quay lại menu...")

# Hàm thay đổi đơn đặt phòng (edit booking cho admin)
def admin_edit_booking(db: Session):
    print("\n--- THAY ĐỔI ĐƠN ĐẶT PHÒNG ---")
    booking_id = int(input("Mã booking cần sửa: "))

    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        print("Không tìm thấy booking!")
        return

    check_in_str = input("Ngày nhận phòng mới (YYYY-MM-DD, Enter bỏ qua): ").strip() or None
    check_out_str = input("Ngày trả phòng mới (YYYY-MM-DD, Enter bỏ qua): ").strip() or None
    phone = input("SĐT mới (Enter bỏ qua): ").strip() or None
    total_amount = input("Tổng tiền mới (Enter bỏ qua): ").strip()
    total_amount = float(total_amount) if total_amount else None
    notes = input("Ghi chú mới (Enter bỏ qua): ").strip() or None

    try:
        updated_booking = edit_booking(
            db=db,
            booking_id=booking_id,
            check_in=check_in_str,
            check_out=check_out_str,
            phone=phone,
            total_amount=total_amount,
            notes=notes
        )
        print(f"Chỉnh sửa booking #{updated_booking.id} thành công!")
    except ValueError as e:
        print(f"Lỗi: {e}")

def admin_view_rooms(db: Session):
    print("\n" + "="*80)
    print("                   DANH SÁCH TẤT CẢ CÁC PHÒNG")
    print("="*80)
    
    rooms = db.query(Room).order_by(Room.room_number).all()
    
    if not rooms:
        print("  Chưa có phòng nào trong hệ thống!")
        print("="*80)
        input("\nNhấn Enter để quay lại...")
        return

    print(f"  Tổng cộng: {len(rooms)} phòng")
    print("-" * 80)
    
    for r in rooms:
        status_vn = {
            RoomStatus.available: "Trống",
            RoomStatus.booked: "Đã đặt"
        }.get(r.status, "Không rõ")
        
        print(f"  [{r.id:2}] {r.room_number:6} | {r.type:8} | {r.price_per_night:,.0f}đ/đêm | {r.max_occupancy} người | {status_vn}")
        if r.description:
            print(f"       → {r.description}")
        print("       Tiện ích:", r.amenities or "Cơ bản")
        print("-" * 80)

    input("\nNhấn Enter để quay lại menu...")