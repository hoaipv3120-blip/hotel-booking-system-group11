from sqlalchemy import Column, Integer, String, Date, Enum
from models.base import Base
import enum

class Gender(enum.Enum):
    male = "male"
    female = "female"
    other = "other"

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    gender = Column(Enum(Gender))
    dob = Column(Date)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String)
    password_hash = Column(String, nullable=False)
    address = Column(String)