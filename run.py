import os
import sys
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

sys.path.append("/app")  
sys.path.append("/app/src")

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://hoteluser:hotel123@db:5432/hoteldb")

# Retry kết nối DB
for i in range(15):
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            print("Kết nối database thành công!")
        break
    except OperationalError:
        print(f"Đang chờ PostgreSQL khởi động... ({i+1}/15)")
        time.sleep(2)
else:
    print("Không thể kết nối database!")
    exit(1)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from src.main import main
main()