import os
from services.room_service import add_room
from models.room import Room

def load_rooms_from_file(db, file_name="rooms.txt"):
    # LẤY ĐƯỜNG DẪN TỪ GỐC DỰ ÁN (cùng cấp với src/)
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    file_path = os.path.join(base_dir, file_name)

    print(f"Đang tìm file: {file_path}")  # DEBUG

    if not os.path.exists(file_path):
        print(f"Không tìm thấy file: {file_path}")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    added_count = 0
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        parts = [p.strip() for p in line.split(",")]
        if len(parts) < 4:
            print(f"Dòng {line_num}: Thiếu dữ liệu → {line}")
            continue

        room_number = parts[0]
        room_type = parts[1]
        price = float(parts[2])
        max_occupancy = int(parts[3])
        description = parts[4] if len(parts) > 4 else ""
        amenities = ", ".join(parts[5:]) if len(parts) > 5 else ""

        # KIỂM TRA PHÒNG ĐÃ TỒN TẠI CHƯA
        if db.query(Room).filter(Room.room_number == room_number).first():
            continue

        try:
            add_room(
                db=db,
                room_number=room_number,
                type=room_type,
                price_per_night=price,
                max_occupancy=max_occupancy,
                description=description,
                amenities=amenities
            )
            added_count += 1
        except Exception as e:
            print(f"Dòng {line_num}: Lỗi → {e}")

    print(f"Đã thêm {added_count} phòng từ file!")