from sqlalchemy.orm import Session
from models.booking import Booking, BookingStatus
from models.room import Room
from datetime import date
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
#from models.customer import Customer

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
        status=BookingStatus.Confirmed
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    print(f"Đặt phòng thành công! Mã: #{booking.id} | Trạng thái: Confirmed")
    return booking

def send_confirmation_email(booking: Booking, room: Room):
    sender = "hotel.group11@gmail.com"
    password = "your_app_password"  # Dùng App Password nếu Gmail
    recipient = booking.customer.email

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = f"Xác nhận đặt phòng #{booking.id} - Khách sạn Nhóm 11"

    body = f"""
    <h2>XÁC NHẬN ĐẶT PHÒNG THÀNH CÔNG</h2>
    <p><strong>Khách hàng:</strong> {booking.customer.name}</p>
    <p><strong>Phòng:</strong> {room.room_number} ({room.type})</p>
    <p><strong>Nhận phòng:</strong> {booking.check_in}</p>
    <p><strong>Trả phòng:</strong> {booking.check_out}</p>
    <p><strong>Tổng tiền:</strong> {booking.total_amount:,.0f} VND</p>
    <p><strong>Ghi chú:</strong> {booking.notes or 'Không có'}</p>
    <hr>
    <p>Cảm ơn quý khách đã tin tưởng!</p>
    """
    msg.attach(MIMEText(body, "html"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())
        server.quit()
        print("Đã gửi email xác nhận!")
    except Exception as e:
        print(f"Không gửi được email: {e}")

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

def get_all_bookings(db: Session):
    """Lấy tất cả booking (dành cho Admin)"""
    return db.query(Booking).order_by(Booking.id.desc()).all()

# Thêm vào src/services/booking_service.py

def edit_booking(db: Session, booking_id: int, check_in: str = None, check_out: str = None, phone: str = None, total_amount: float = None, notes: str = None) -> Booking:
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise ValueError("Booking không tồn tại!")

    if check_in:
        booking.check_in = datetime.strptime(check_in, "%Y-%m-%d").date()
    if check_out:
        booking.check_out = datetime.strptime(check_out, "%Y-%m-%d").date()
    if phone:
        booking.customer.phone = phone  # Cập nhật phone của customer
    if total_amount is not None:
        booking.total_amount = total_amount
    if notes is not None:
        booking.notes = notes

    db.commit()
    db.refresh(booking)
    return booking

def cancel_booking(db: Session, booking_id: int) -> Booking:
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise ValueError("Booking không tồn tại!")

    if booking.status != BookingStatus.confirmed:
        raise ValueError("Chỉ có thể hủy khi trạng thái là New!")

    booking.status = BookingStatus.cancelled
    db.commit()
    db.refresh(booking)
    return booking
'''
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
            "Confirmed": "Đã xác nhận",
            "Cancelled": "Đã hủy"
        }.get(b.status.value, "Không rõ")

        print(f"  #{b.id} | Khách: {b.customer.name} ({b.customer.email})")
        print(f"     Phòng: {b.room.room_number} ({b.room.type})")
        print(f"     Thời gian: {b.check_in} → {b.check_out}")
        print(f"     Tổng tiền: {b.total_amount:,.0f} VND")
        print(f"     Trạng thái: {status_icon}")
        if b.notes:
            print(f"     Ghi chú: {b.notes}")
        print("-" * 80)

    input("\nNhấn Enter để quay lại menu...")
    '''