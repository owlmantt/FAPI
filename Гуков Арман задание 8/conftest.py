import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database import Base, get_db
import models

# Создаем тестовую базу данных в памяти
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def test_db():
    # Создаем таблицы перед каждым тестом
    Base.metadata.create_all(bind=engine)
    try:
        yield TestingSessionLocal()
    finally:
        # Удаляем таблицы после каждого теста
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def test_user(client):
    user_data = {
        "username": "testuser",
        "password": "testpass"
    }
    response = client.post("/register", json=user_data)
    assert response.status_code == 200
    return user_data

@pytest.fixture
def test_user_token(client, test_user):
    response = client.post("/token", json=test_user)
    assert response.status_code == 200
    token = response.json()["access_token"]
    return token

@pytest.fixture
def authorized_client(client, test_user_token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {test_user_token}"
    }
    return client

@pytest.fixture
def test_notes(authorized_client):
    notes_data = [
        {"title": f"test title {i}", "content": f"test content {i}"} 
        for i in range(3)
    ]
    
    responses = []
    for note in notes_data:
        response = authorized_client.post("/notes/", json=note)
        assert response.status_code == 200
        responses.append(response.json())
    
    return responses 