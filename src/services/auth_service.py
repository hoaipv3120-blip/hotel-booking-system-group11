import bcrypt
from sqlalchemy.orm import Session
from models.customer import Customer
from datetime import datetime

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

def register(db: Session, **data):
    if db.query(Customer).filter(Customer.email == data["email"]).first():
        raise ValueError("Email đã tồn tại")
    
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

def is_admin(customer: Customer) -> bool:
    """Kiểm tra xem user có phải admin không (dựa vào email)"""
    return customer.email in ["admin@gmail.com"]