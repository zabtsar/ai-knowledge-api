from jose import jwt

from app.auth import (
    create_access_token,
    SECRET_KEY,
    ALGORITHM
)

def test_create_access_token():
    data = {"sub": "testuser", "role": "user"}

    token = create_access_token(data)

    assert isinstance(token, str)
    assert len(token) > 0

def test_decode_access_token():
    data = {"sub": "testuser", "role": "user"}

    token = create_access_token(data)

    decoded = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    assert decoded["sub"] == "testuser"
    assert decoded["role"] == "user"
    assert "exp" in decoded