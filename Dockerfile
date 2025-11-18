# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy toàn bộ code
COPY . .

# CÀI TẤT CẢ CÁC PACKAGE CẦN THIẾT
RUN pip install --no-cache-dir sqlalchemy bcrypt

# Chạy chương trình
CMD ["python", "run.py"]