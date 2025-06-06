import pytest
from fastapi import status

def test_create_note(authorized_client):
    response = authorized_client.post(
        "/notes/",
        json={"title": "test title", "content": "test content"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "test title"
    assert data["content"] == "test content"
    assert "id" in data
    assert "owner_id" in data

def test_create_note_unauthorized(client):
    response = client.post(
        "/notes/",
        json={"title": "test title", "content": "test content"}
    )
    assert response.status_code == 401

def test_get_notes(authorized_client, test_notes):
    response = authorized_client.get("/notes/")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == len(test_notes)
    assert data["total"] == len(test_notes)
    assert data["has_more"] == False

def test_get_notes_with_search(authorized_client, test_notes):
    response = authorized_client.get("/notes/?search=title 1")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["title"] == "test title 1"

def test_get_note_by_id(authorized_client, test_notes):
    note_id = test_notes[0]["id"]
    response = authorized_client.get(f"/notes/{note_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == note_id
    assert data["title"] == test_notes[0]["title"]
    assert data["content"] == test_notes[0]["content"]

def test_get_note_not_found(authorized_client):
    response = authorized_client.get("/notes/999")
    assert response.status_code == 404

def test_update_note(authorized_client, test_notes):
    note_id = test_notes[0]["id"]
    updated_data = {
        "title": "updated title",
        "content": "updated content"
    }
    response = authorized_client.put(f"/notes/{note_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == updated_data["title"]
    assert data["content"] == updated_data["content"]

def test_update_note_not_found(authorized_client):
    response = authorized_client.put(
        "/notes/999",
        json={"title": "updated title", "content": "updated content"}
    )
    assert response.status_code == 404

def test_delete_note(authorized_client, test_notes):
    note_id = test_notes[0]["id"]
    response = authorized_client.delete(f"/notes/{note_id}")
    assert response.status_code == 200
    
    # Проверяем, что заметка действительно удалена
    response = authorized_client.get(f"/notes/{note_id}")
    assert response.status_code == 404

def test_delete_note_not_found(authorized_client):
    response = authorized_client.delete("/notes/999")
    assert response.status_code == 404

def test_pagination(authorized_client):
    # Создаем 15 заметок
    for i in range(15):
        authorized_client.post(
            "/notes/",
            json={"title": f"title {i}", "content": f"content {i}"}
        )
    
    # Проверяем первую страницу (по умолчанию limit=10)
    response = authorized_client.get("/notes/")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 10
    assert data["has_more"] == True
    
    # Проверяем вторую страницу
    response = authorized_client.get("/notes/?skip=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 5
    assert data["has_more"] == False 