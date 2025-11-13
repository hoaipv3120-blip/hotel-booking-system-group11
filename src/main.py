def main_menu():
    print("\n" + "="*60)
    print("   HỆ THỐNG ĐẶT PHÒNG KHÁCH SẠN - NHÓM 11")
    print("="*60)
    print("1. Đăng nhập")
    print("2. Đăng ký")
    print("3. Tìm phòng (khách vãng lai)")
    print("4. Quản trị viên")
    print("0. Thoát")
    print("-"*60)
    return input("Chọn chức năng: ")

if __name__ == "__main__":
    choice = main_menu()
    print(f"\nBạn đã chọn: {choice}")
    print("Chức năng đang được phát triển...")