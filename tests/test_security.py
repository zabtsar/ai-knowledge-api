from app.security import hash_password, verify_password


def test_hash_password():
    password = "password123"

    hashed = hash_password(password)

    assert hashed != password
    assert hashed.startswith("$2")


def test_verify_password_correct():
    password = "password123"
    hashed = hash_password(password)

    assert verify_password(password, hashed) is True


def test_verify_password_incorrect():
    password = "password123"
    hashed = hash_password(password)

    assert verify_password("wrongpassword", hashed) is False