import pytest
from fastapi.testclient import TestClient
from api.main import app
import json

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_config(monkeypatch):
    monkeypatch.setattr("api.routes.files.load_config", lambda: {"api_id": 123, "api_hash": "abc"})

@pytest.fixture(autouse=True)
def mock_telegram_client(monkeypatch):
    class MockClient:
        async def __aenter__(self):
            return self
        async def __aexit__(self, exc_type, exc, tb):
            pass
        async def start(self):
            pass
    monkeypatch.setattr("api.routes.files.get_configured_client", lambda: MockClient())

@pytest.fixture(autouse=True)
def mock_services(monkeypatch):
    async def mock_upload_file(*args, **kwargs):
        return {"id": 1, "name": "test.txt", "size": "100B", "path": "/"}

    async def mock_download_file(*args, **kwargs):
        import tempfile
        import os
        fd, path = tempfile.mkstemp(suffix=".txt")
        with os.fdopen(fd, 'w') as f:
            f.write("test content")
        return path

    async def mock_delete_file(client, file_id):
        if file_id == 999:
            from utils.errors import TSGError
            raise TSGError("File not found")
        return True

    monkeypatch.setattr("api.routes.files.upload_file", mock_upload_file)
    monkeypatch.setattr("api.routes.files.download_file", mock_download_file)
    monkeypatch.setattr("api.routes.files.delete_file", mock_delete_file)

@pytest.fixture(autouse=True)
def mock_metadata_manager(monkeypatch):
    monkeypatch.setattr("api.routes.files.add_tag", lambda file_id, tag: None)
    monkeypatch.setattr("api.routes.files.remove_tag", lambda file_id, tag: None)

def test_upload_file():
    with open("test_upload.txt", "w") as f:
        f.write("test")
    with open("test_upload.txt", "rb") as f:
        response = client.post("/files/upload?path=/test", files={"file": ("test_upload.txt", f, "text/plain")})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["id"] == 1
    assert data["data"]["path"] == "/"
    import os
    os.remove("test_upload.txt")

def test_download_file():
    response = client.get("/files/download/1")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/octet-stream"
    assert b"test content" in response.content

def test_delete_file():
    response = client.delete("/files/1")
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_delete_file_invalid():
    response = client.delete("/files/999")
    assert response.status_code == 200
    assert response.json()["status"] == "error"

def test_delete_files_batch():
    response = client.delete("/files/?ids=1,2")
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["data"]["deleted"] == 2

def test_tag_files_add():
    response = client.post("/files/tag", json={"file_ids": [1, 2], "tag": "important", "action": "add"})
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["data"]["tagged"] == 2

def test_tag_files_remove():
    response = client.post("/files/tag", json={"file_ids": [1, 2], "tag": "important", "action": "remove"})
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["data"]["tagged"] == 2

def test_tag_files_invalid_action():
    response = client.post("/files/tag", json={"file_ids": [1, 2], "tag": "important", "action": "invalid"})
    assert response.status_code == 200
    assert response.json()["status"] == "error"
