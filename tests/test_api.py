from fastapi.testclient import TestClient
from app.main import app
from app.models.models import Collection, CollectionCreate
import json

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Qdrant FastAPI application!"}


def test_list_collection():
    """Test creating a new collection."""
    response = client.get(
        "/qdrant/collections/",
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Collections found"


def test_create_collection():
    """Test creating a new collection."""
    data = {"name": "test_collection", "dimensions": "3", "distance": "cosine"}

    response = client.post(
        "/qdrant/collections/",
        content=json.dumps(data),
        headers={"content-type": "application/json", "accept": "appication/json"},
    )

    assert response.status_code == 201
    assert response.json()["message"] == "Collection created successfully"


def test_upload_document():
    data = '{"id": 1, "metadata": {"test": "document"}, "vector": [0.5, 0.4, 0.1]}'

    response = client.post(
        "/qdrant/test_collection",
        content=data,
        headers={"content-type": "application/json", "accept": "appication/json"},
    )

    assert response.status_code == 201
    assert response.json()["message"] == "Document uploaded"


def test_get_document():
    response = client.get(
        "/qdrant/test_collection/1",
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Document found"


def test_update_document():
    data = '{"id": 1, "metadata": {"test": "document"}, "vector": [0.2, 0.2, 0.2]}'

    response = client.post(
        "/qdrant/test_collection/update",
        content=data,
        headers={"content-type": "application/json", "accept": "appication/json"},
    )

    assert response.status_code == 201
    assert response.json()["message"] == "Document updated"


def test_delete_document():
    response = client.delete(
        "/qdrant/test_collection/1",
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Document deleted"


def test_get_collection_info():
    response = client.get("/qdrant/collections/test_collection")

    assert response.status_code == 200
    assert response.json()["message"] == "Collection found"


def test_delete_collection():
    response = client.delete("/qdrant/collections/test_collection")

    assert response.status_code == 202
    assert response.json()["message"] == "Collection deleted"


def test_encode_text():
    response = client.post("/qdrant/encode/?text=This%20is%20a%20test")

    assert response.status_code == 200
    assert response.json()["message"] == "Text encoded"
    assert response.json()["details"]["text"] == "This is a test"
