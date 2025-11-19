# Dockerfile - PHIÊN BẢN CHUẨN 100%
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy requirements.txt trước để tận dụng cache
COPY requirements.txt .

# CÀI TỪ requirements.txt (KHÔNG CÀI TRỰC TIẾP Ở ĐÂY NỮA!)
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code
COPY . .

# Chạy chương trình
CMD ["python", "run.py"]