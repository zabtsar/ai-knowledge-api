from app import models
from app.security import hash_password


def register_user(client, username="testuser"):
    return client.post(
        "/auth/register",
        json={
            "username": username,
            "email": f"{username}@example.com",
            "password": "Password123!"
        }
    )


def login_user(client, username="testuser"):
    response = client.post(
        "/auth/login",
        json={
            "username": username,
            "password": "Password123!"
        }
    )
    return response.json()["access_token"]


def test_register_user(client):
    response = register_user(client)

    assert response.status_code == 201
    assert response.json()["username"] == "testuser"
    assert response.json()["role"] == "user"
    assert "password_hash" not in response.json()


def test_login_success(client):
    register_user(client)

    response = client.post(
        "/auth/login",
        json={
            "username": "testuser",
            "password": "Password123!"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_wrong_password(client):
    register_user(client)

    response = client.post(
        "/auth/login",
        json={
            "username": "testuser",
            "password": "WrongPassword123!"
        }
    )

    assert response.status_code == 401


def test_user_can_access_user_dashboard(client):
    register_user(client)
    token = login_user(client)

    response = client.get(
        "/user/dashboard",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["role"] == "user"


def test_user_cannot_access_admin_dashboard(client):
    register_user(client)
    token = login_user(client)

    response = client.get(
        "/admin/dashboard",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403


def test_admin_can_access_admin_dashboard(client, db):
    admin = models.User(
        username="admin_test",
        email="admin@example.com",
        password_hash=hash_password("Password123!"),
        role="admin"
    )

    db.add(admin)
    db.commit()

    response = client.post(
        "/auth/login",
        json={
            "username": "admin_test",
            "password": "Password123!"
        }
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    dashboard_response = client.get(
        "/admin/dashboard",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert dashboard_response.status_code == 200
    assert dashboard_response.json()["role"] == "admin"


def test_admin_can_access_user_dashboard(client, db):
    admin = models.User(
        username="admin_test",
        email="admin@example.com",
        password_hash=hash_password("Password123!"),
        role="admin"
    )

    db.add(admin)
    db.commit()

    token = login_user(client, "admin_test")

    response = client.get(
        "/user/dashboard",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["role"] == "admin"


def test_dashboard_without_token(client):
    response = client.get("/admin/dashboard")

    assert response.status_code == 401

def test_register_invalid_email(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "bukan-email",
            "password": "password123"
        }
    )

    assert response.status_code == 422


def test_register_short_password(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "123"
        }
    )

    assert response.status_code == 422


def test_register_invalid_username(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "test user!",
            "email": "test@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 422