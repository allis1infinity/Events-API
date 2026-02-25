from models import User

def test_user_password_hashing_behaves_correctly():
    kira = User(username="kira")
    password = "<PASSWORD_123>"

    kira.set_password(password)

    assert kira.password_hash is not None
    assert kira.password_hash != password

    assert kira.check_password(password) is True
    assert kira.check_password("<PASSWORD>") is False