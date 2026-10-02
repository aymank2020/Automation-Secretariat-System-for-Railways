import pytest

from app.core.security import create_access_token


def test_public_registration_is_rejected(client):
    response = client.post("/auth/register", json={"username": "intruder", "password": "test-password", "seclevel": "admin"})
    assert response.status_code in (401, 403)


def test_regular_user_cannot_register_an_admin(client):
    token = client.post("/auth/login", json={"username": "user", "password": "test-password"}).json()["access_token"]
    response = client.post("/auth/register", json={"username": "intruder", "password": "test-password", "seclevel": "admin"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403


def test_admin_can_register_and_new_user_can_login(client):
    token = client.post("/auth/login", json={"username": "admin", "password": "test-password"}).json()["access_token"]
    response = client.post("/auth/register", json={"username": "new-user", "password": "new-password", "seclevel": "superuser"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["seclevel"] == "user"
    assert client.post("/auth/login", json={"username": "new-user", "password": "new-password"}).status_code == 200


@pytest.mark.parametrize("subject", [None, "invalid", "0", "-1"])
def test_invalid_token_subject_returns_401(client, subject):
    token = create_access_token({"sub": subject} if subject is not None else {})
    assert client.get("/documents/", headers={"Authorization": f"Bearer {token}"}).status_code == 401
