import pytest
from fastapi import status

def test_register_user(client):
    response = client.post(
        "/register",
        json={"username": "testuser1", "password": "testpass1"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser1"
    assert "password" not in data

def test_register_duplicate_user(client, test_user):
    response = client.post(
        "/register",
        json={"username": test_user["username"], "password": "testpass"}
    )
    assert response.status_code == 400

def test_login_user(client, test_user):
    response = client.post(
        "/token",
        json=test_user
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client, test_user):
    response = client.post(
        "/token",
        json={
            "username": test_user["username"],
            "password": "wrongpass"
        }
    )
    assert response.status_code == 401

def test_get_current_user(authorized_client):
    response = authorized_client.get("/users/me")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"

def test_get_current_user_without_token(client):
    response = client.get("/users/me")
    assert response.status_code == 401 