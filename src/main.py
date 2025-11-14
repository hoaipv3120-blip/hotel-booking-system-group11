from database.db import SessionLocal, Base, engine
from services.auth_service import register
from services.room_service import search_rooms
from services.booking_service import create_booking
from controllers.admin_controller import admin_add_room
from datetime import datetime
from services.auth_service import register, login
from utils.load_rooms import load_rooms_from_file  # ← THÊM DÒNG NÀY
from services.room_service import search_rooms, get_room_by_number
from services.auth_service import login, is_admin

# TẠO BẢNG KHI CHẠY LẦN ĐẦU
Base.metadata.create_all(bind=engine)

def main():
    db = SessionLocal()
    
    # BƯỚC 1: TẠO BẢNG TRƯỚC
    Base.metadata.create_all(bind=engine)  # ← TẠO BẢNG

    # BƯỚC 2: SAU ĐÓ MỚI NẠP DỮ LIỆU
    try:
        load_rooms_from_file(db, "rooms.txt")  # ← ĐỌC FILE SAU KHI CÓ BẢNG
    except Exception as e:
        print(f"Lỗi khi nạp phòng: {e}")
    try:
        print("=== HỆ THỐNG ĐẶT PHÒNG KHÁCH SẠN - NHÓM 11 ===")
        
        while True:
            print("\nBạn là:")
            print("1. Khách hàng")
            print("2. Admin")
            role_choice = input("Chọn (1/2): ").strip()

            current_user = None

            if role_choice == "2":
            # === ĐĂNG NHẬP ADMIN ===
                print("\n--- ĐĂNG NHẬP ADMIN ---")
                email = input("Email admin: ").strip()
                password = input("Mật khẩu: ").strip()
                try:
                    current_user = login(db, email, password)
                    if not is_admin(current_user):
                        print("Bạn không có quyền admin!")
                        continue
                    print(f"Chào Admin {current_user.name}!")
                except ValueError as e:
                    print(f"Lỗi: {e}")
                    continue

            else:
            # === ĐĂNG NHẬP KHÁCH HÀNG ===
                print("\n--- ĐĂNG NHẬP KHÁCH HÀNG ---")
                email = input("Email: ").strip()
                password = input("Mật khẩu: ").strip()
                try:
                    current_user = login(db, email, password)
                    print(f"Chào {current_user.name}!")
                except ValueError as e:
                    print(f"Lỗi: {e}")
                    continue

        # === MENU RIÊNG THEO VAI TRÒ ===
            while True:
                if is_admin(current_user):
                    # MENU ADMIN
                    print("\n" + "="*50)
                    print("           MENU ADMIN")
                    print("="*50)
                    print("1. Tìm phòng")
                    print("2. Thêm phòng mới")
                    print("3. Xem tất cả booking")
                    print("0. Đăng xuất")
                    print("="*50)
                    choice = input("Chọn: ").strip()
                else:
                # MENU KHÁCH HÀNG
                    print("\n" + "="*50)
                    print("         MENU KHÁCH HÀNG")
                    print("="*50)
                    print("1. Tìm phòng")
                    print("2. Đặt phòng")
                    print("3. Xem booking của tôi")
                    print("0. Đăng xuất")
                    print("="*50)
                    choice = input("Chọn: ").strip()

            # === CHUNG CHO CẢ 2 ===
                if choice == "1":
                # TÌM PHÒNG + XEM CHI TIẾT
                    print("\n--- TÌM PHÒNG TRỐNG ---")
                    rooms = search_rooms(db)
                    if not rooms:
                        print("Không có phòng nào!")
                        continue

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
                    print(f"\nChi tiết {room.room_number}: {room.type}, {room.price_per_night:,} VND, {room.max_occupancy} người")
                    if room.description:
                        print(f"Mô tả: {room.description}")
                    if room.amenities:
                        print(f"Tiện ích: {room.amenities}")

                    elif choice == "2" and is_admin(current_user):
                        admin_add_room(db)

                    elif choice == "2" and not is_admin(current_user):
                        print("Chức năng đặt phòng (sẽ viết sau)")

                    elif choice == "0":
                        print("Đã đăng xuất!")
                        break

                    else:
                        print("Lựa chọn không hợp lệ!")

    except KeyboardInterrupt:
        print("\nĐã dừng chương trình.")
    finally:
        db.close()

if __name__ == "__main__":
    main()