def test_register_login(db_session):
    from services.auth_service import register, login
    user = register(db_session, name="Test", email="test@gmail.com", password="123",
                    gender="male", dob="2000-01-01", phone="0123", address="HN")
    logged_in = login(db_session, "test@gmail.com", "123")
    assert logged_in.id == user.id
#python src/main.py