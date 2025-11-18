# === IMPORTS ===
from sqlalchemy.orm import Session
from database.db import SessionLocal, engine
from models.base import Base
from utils.load_rooms import load_rooms_from_file
from services.auth_service import login, register, is_admin
from services.room_service import search_rooms, get_room_by_number
from controllers.admin_controller import admin_add_room, admin_edit_room, admin_delete_room, admin_view_customers, admin_edit_booking
#from services.booking_service import create_booking
from models.room import Room
from services.booking_service import create_booking, get_bookings_by_customer, cancel_booking, get_all_bookings
from datetime import datetime, date  # ← THÊM `date`
from models.customer import Customer
#from controllers.admin_controller import admin_view_customers, admin_edit_booking #, admin_cancel_booking
#from sqlalchemy import text
from models.booking import Booking, BookingStatus

# ========================================
# HÀM RIÊNG - PHẢI ĐỊNH NGHĨA TRƯỚC KHI DÙNG
# ========================================

def upgrade_database_schema(db):
    """Tự động thêm cột is_admin nếu thiếu"""
    inspector = db.inspect(db.engine)
    columns = [col["name"] for col in inspector.get_columns("customers")]
    if "is_admin" not in columns:
        print("Đang cập nhật DB: thêm cột is_admin...")
        with db.engine.connect() as conn:
            conn.execute(text("ALTER TABLE customers ADD COLUMN is_admin BOOLEAN DEFAULT FALSE"))
            conn.commit()
        print("Cập nhật thành công!")

def admin_view_all_bookings(db):
    print("\n" + "="*80)
    print("                DANH SÁCH TẤT CẢ BOOKING")
    print("="*80)
    
    bookings = get_all_bookings(db)
    
    if not bookings:
        print("  Chưa có booking nào!")
        print("="*80)
        input("\nNhấn Enter để tiếp tục...")
        return

    for b in bookings:
        status_icon = {
            BookingStatus.confirmed: "Đã xác nhận",
            BookingStatus.cancelled: "Đã hủy"
        }.get(b.status, "Không rõ")

        print(f"  #{b.id} | Khách: {b.customer.name} ({b.customer.email})")
        print(f"     Phòng: {b.room.room_number} ({b.room.type})")
        print(f"     Thời gian: {b.check_in} → {b.check_out}")
        print(f"     Tổng tiền: {b.total_amount:,.0f} VND")
        print(f"     Trạng thái: {status_icon}")
        if b.notes:
            print(f"     Ghi chú: {b.notes}")
        print("-" * 80)

    input("\nNhấn Enter để quay lại menu...")

def admin_menu(db):
    print("\n--- ĐĂNG NHẬP ADMIN ---")
    email = input("Email admin: ").strip()
    password = input("Mật khẩu: ").strip()

    try:
        user = login(db, email, password)
        if not is_admin(user):
            print("Bạn không có quyền admin!")
            return
        print(f"Chào Admin {user.name}!")

        while True:
            print("\n" + "="*50)
            print("           MENU ADMIN")
            print("="*50)
            print("1. Quản lý phòng")
            print("2. Quản lý khách hàng")
            print("3. Quản lý booking")
            print("0. Đăng xuất")
            print("="*50)
            choice = input("Chọn: ").strip()

            if choice == "1":
                admin_manage_room(db)
            elif choice == "2":
                admin_manage_customer(db)
            elif choice == "3":
                admin_manage_booking(db)
            elif choice == "0":
                print("Đã đăng xuất!")
                break
            else:
                print("Lựa chọn không hợp lệ!")

    except ValueError as e:
        print(f"Lỗi: {e}")

def ensure_admin_exists(db):
    from services.auth_service import register
    admin = db.query(Customer).filter(Customer.email == "admin@gmail.com").first()
    if not admin:
        register(
            db=db,
            name="Quản Trị Viên",
            email="admin@gmail.com",
            password="admin123",
            gender="other",
            dob="1970-01-01",
            phone="0000000000",
            address="Hotel HQ",
            is_admin=True
        )
        #db.add(admin)
        #db.commit()

        print("Tạo Admin: admin@gmail.com / admin123")

# Hàm quản lý room (sub-menu cho admin)
def admin_manage_room(db):
    while True:
        print("\n" + "="*50)
        print("           QUẢN LÝ PHÒNG")
        print("="*50)
        print("1. Thêm phòng mới")
        print("2. Chỉnh sửa phòng")
        print("3. Xóa phòng")
        print("0. Quay lại menu Admin")
        print("="*50)
        choice = input("Chọn: ").strip()

        if choice == "1":
            admin_add_room(db)
        elif choice == "2":
            admin_edit_room(db)
        elif choice == "3":
            admin_delete_room(db)
        elif choice == "0":
            break
        else:
            print("Lựa chọn không hợp lệ!")

# Hàm quản lý customer (sub-menu cho admin)
def admin_manage_customer(db):
    while True:
        print("\n" + "="*50)
        print("           QUẢN LÝ KHÁCH HÀNG")
        print("="*50)
        print("1. Xem danh sách khách hàng")
        print("0. Quay lại menu Admin")
        print("="*50)
        choice = input("Chọn: ").strip()

        if choice == "1":
            admin_view_customers(db)
        elif choice == "0":
            break
        else:
            print("Lựa chọn không hợp lệ!")

# Hàm quản lý booking (sub-menu cho admin)
def admin_manage_booking(db):
    while True:
        print("\n" + "="*50)
        print("           QUẢN LÝ BOOKING")
        print("="*50)
        print("1. Xem danh sách booking")
        print("2. Thay đổi đơn đặt phòng")
        print("3. Hủy đơn đặt phòng")
        print("0. Quay lại menu Admin")
        print("="*50)
        choice = input("Chọn: ").strip()

        if choice == "1":
            admin_view_all_bookings(db)
        elif choice == "2":
            admin_edit_booking(db)
        elif choice == "3":
            #admin_cancel_booking(db)
            print("\n--- HỦY ĐƠN ĐẶT PHÒNG (ADMIN) ---")
            try:
                booking_id = int(input("Nhập mã booking cần hủy: "))
                cancel_booking(db, booking_id)  # ← DÙNG CHUNG HÀM, KHÔNG CẦN HÀM RIÊNG
            except ValueError as e:
                print(f"Lỗi: {e}")
                input("Nhấn Enter để tiếp tục...")
        elif choice == "0":
            break
        else:
            print("Lựa chọn không hợp lệ!")

def customer_menu(db, user):
    while True:
        print("\n" + "="*50)
        print("         MENU KHÁCH HÀNG")
        print("="*50)
        print("1. Tìm phòng")
        print("2. Đặt phòng")
        print("3. Xem booking của tôi")
        print("0. Đăng xuất")
        print("="*50)
        choice = input("Chọn: ").strip()

        if choice == "1":
            show_room_search(db)
        elif choice == "2":
            book_room_flow(db, user)  # ← ĐÃ ĐỊNH NGHĨA TRƯỚC → OK!
        elif choice == "3":
            view_my_bookings(db, user)
        elif choice == "0":
            print("Đã đăng xuất!")
            break
        else:
            print("Lựa chọn không hợp lệ!")

def register_form(db):
    print("\n--- ĐĂNG KÝ TÀI KHOẢN ---")
    while True:
        dob_str = input("Ngày sinh (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(dob_str, "%Y-%m-%d")
            break
        except ValueError:
            print("Lỗi: Nhập đúng định dạng YYYY-MM-DD (ví dụ: 2000-02-06)")

    data = {
        "name": input("Họ tên: ").strip(),
        "email": input("Email: ").strip(),
        "password": input("Mật khẩu: ").strip(),
        "gender": input("Giới tính (male/female/other): ").strip().lower(),
        "dob": dob_str,
        "phone": input("SĐT: ").strip(),
        "address": input("Địa chỉ: ").strip()
    }

    try:
        register(db, **data)
        return True
    except Exception as e:
        print(f"Lỗi: {e}")
        return False


def customer_login(db):
    print("\n--- ĐĂNG NHẬP KHÁCH HÀNG ---")
    email = input("Email: ").strip()
    password = input("Mật khẩu: ").strip()
    try:
        user = login(db, email, password)
        print(f"Chào {user.name}!")
        return user
    except ValueError as e:
        print(f"Lỗi: {e}")
        return None


def book_room_flow(db, user):
    print("\n--- ĐẶT PHÒNG ---")
    rooms = search_rooms(db)
    if not rooms:
        print("Hiện không có phòng trống!")
        return

    print("Danh sách phòng trống:")
    for r in rooms:
        print(f"  [{r.id}] {r.room_number} | {r.type} | {r.price_per_night:,} VND/đêm")

    try:
        room_id = int(input("\nChọn ID phòng: ").strip())
        room = db.query(Room).filter(Room.id == room_id).first()
        if not room:
            print("Phòng không tồn tại!")
            return

        check_in_str = input("Ngày nhận phòng (YYYY-MM-DD): ").strip()
        check_out_str = input("Ngày trả phòng (YYYY-MM-DD): ").strip()

        check_in = datetime.strptime(check_in_str, "%Y-%m-%d").date()
        check_out = datetime.strptime(check_out_str, "%Y-%m-%d").date()

        if check_in >= check_out:
            print("Ngày trả phòng phải sau ngày nhận phòng!")
            return
        if check_in < date.today():
            print("Không thể đặt ngày trong quá khứ!")
            return

        notes = input("Ghi chú (nếu có): ").strip()

        booking = create_booking(
            db=db,
            customer_id=user.id,
            room_id=room.id,
            check_in=check_in,
            check_out=check_out,
            notes=notes
        )

        print("\n" + "="*50)
        print("        ĐẶT PHÒNG THÀNH CÔNG!")
        print("="*50)
        print(f"  Mã đặt phòng: #{booking.id}")
        print(f"  Phòng: {room.room_number} ({room.type})")
        print(f"  Thời gian: {check_in} → {check_out}")
        print(f"  Tổng tiền: {booking.total_amount:,.0f} VND")
        print("="*50)

    except ValueError as e:
        print(f"Lỗi định dạng: {e}")
    except Exception as e:
        print(f"Đặt phòng thất bại: {e}")

def show_room_search(db):
    print("\n--- TÌM PHÒNG TRỐNG ---")
    rooms = search_rooms(db)
    if not rooms:
        print("Không có phòng nào!")
        return
    print(f"Tìm thấy {len(rooms)} phòng:")
    for r in rooms:
        print(f"  [{r.id}] {r.room_number} | {r.type} | {r.price_per_night:,} VND")
    while True:
        detail = input("\nNhập số phòng để xem chi tiết (0 để thoát): ").strip()
        if detail == "0":
            break
        room = get_room_by_number(db, detail)
        if not room:
            print("Không tìm thấy phòng!")
            continue
        print(f"\nChi tiết {room.room_number}: {room.type}, {r.price_per_night:,} VND, {room.max_occupancy} người")
        if room.description:
            print(f"Mô tả: {room.description}")
        if room.amenities:
            print(f"Tiện ích: {room.amenities}")

def view_my_bookings(db, user):
    print("\n" + "="*60)
    print("           DANH SÁCH BOOKING CỦA BẠN")
    print("="*60)

    bookings = get_bookings_by_customer(db, user.id)
    if not bookings:
        print("  Bạn chưa có booking nào!")
        print("="*60)
        input("\nNhấn Enter để quay lại...")
        return

    for b in bookings:
        status = {
            #"New": "New",
            "Confirmed": "Confirmed",
            "Cancelled": "Cancelled"
        }.get(b.status.value, "Confirmed")

        print(f"  {status} Mã: #{b.id}")
        print(f"     Phòng: {b.room.room_number} ({b.room.type})")
        print(f"     Thời gian: {b.check_in} → {b.check_out}")
        print(f"     Tổng tiền: {b.total_amount:,.0f} VND")
        print(f"     Trạng thái: {b.status.value}")
        if b.notes:
            print(f"     Ghi chú: {b.notes}")
        print("-" * 60)

    # === HỦY BOOKING ===
    while True:
        print("Nhập Mã booking để HỦY (0 để thoát): ", end="")
        cancel_id = input().strip()
        if cancel_id == "0":
            break
        try:
            cancel_booking(db, int(cancel_id))  # ← GỌI HÀM MỚI
        except ValueError as e:
            print(f"Lỗi: {e}")
            input("Nhấn Enter để tiếp tục...")

def customer_flow(db):
    while True:
        print("\nBạn đã có tài khoản chưa?")
        print("1. Có (Đăng nhập)")
        print("2. Chưa (Đăng ký)")
        print("0. Quay lại")
        choice = input("Chọn (1/2/0): ").strip()

        if choice == "0":
            return
        elif choice == "2":
            if register_form(db):
                print("Đăng ký thành công! Bây giờ bạn có thể đăng nhập.")
        elif choice == "1":
            user = customer_login(db)
            if user:
                customer_menu(db, user)
                return
        else:
            print("Lựa chọn không hợp lệ!")
        
def main():
    db = SessionLocal()
    Base.metadata.create_all(bind=engine)
    load_rooms_from_file(db, "rooms.txt")
    #debug_print_all_users(db)
    ensure_admin_exists(db)
    #upgrade_database_schema(db)
    print("=== HỆ THỐNG ĐẶT PHÒNG KHÁCH SẠN - NHÓM 11 ===")

    while True:
        print("\nBạn là:")
        print("1. Khách hàng")
        print("2. Admin")
        print("0. Thoát chương trình")
        role = input("Chọn (1/2/0): ").strip()

        if role == "0":
            print("Tạm biệt!")
            break
        elif role == "2":
            admin_menu(db)
        elif role == "1":
            customer_flow(db)
        else:
            print("Lựa chọn không hợp lệ!")


if __name__ == "__main__":
    main()