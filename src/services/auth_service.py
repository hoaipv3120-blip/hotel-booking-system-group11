import bcrypt
from sqlalchemy.orm import Session
from models.customer import Customer
from datetime import datetime

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

def register(db: Session, **data):
    email = data.get("email", "").strip().lower()
    phone = data.get("phone", "").strip()

    # === EMAIL VALIDATE (đã có) ===
    if not email:
        raise ValueError("Email không được để trống!")
    if "@" not in email:
        raise ValueError("Email phải chứa ký tự @")
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        raise ValueError("Email không hợp lệ! Ví dụ đúng: abc@gmail.com")

    # === SỐ ĐIỆN THOẠI: ĐÚNG 10 SỐ + BẮT ĐẦU BẰNG 0 ===
    if not phone:
        raise ValueError("Số điện thoại không được để trống!")
    
    phone_regex = r'^0\d{9}$'
    if not re.match(phone_regex, phone):
        raise ValueError("Số điện thoại phải có đúng 10 số và bắt đầu bằng 0 (VD: 0901234567)")

    # Kiểm tra trùng email
    if db.query(Customer).filter(Customer.email == email).first():
        raise ValueError("Email này đã được sử dụng!")

    # CHUYỂN dob THÀNH date object
    if "dob" in data and isinstance(data["dob"], str):
        data["dob"] = datetime.strptime(data["dob"], "%Y-%m-%d").date()
    
    data["password_hash"] = hash_password(data.pop("password"))
    customer = Customer(**data)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

def login(db: Session, email: str, password: str):
    customer = db.query(Customer).filter(Customer.email == email).first()
    if customer and verify_password(password, customer.password_hash):
        return customer
    raise ValueError("Sai email hoặc mật khẩu")

# services/auth_service.py
def is_admin(customer: Customer):
    return customer.is_admin

import re

def is_valid_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.fullmatch(pattern, email.strip()) is not None