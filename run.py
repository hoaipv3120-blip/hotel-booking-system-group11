# run.py
import sys
import os

# Thêm src vào path để import được
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# Chạy main
from src.main import main

if __name__ == "__main__":
    main()