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
    data = {"name": "test_collection", "dimensions": "2048", "distance": "cosine"}

    response = client.post(
        "/qdrant/collections/",
        content=json.dumps(data),
        headers={"content-type": "application/json", "accept": "appication/json"},
    )

    assert response.status_code == 201
    assert response.json()["message"] == "Collection created successfully"


def test_get_collection_info():
    response = client.get("/qdrant/collections/test_collection")

    assert response.status_code == 200
    assert response.json()["message"] == "Collection found"


def test_delete_collection():
    response = client.delete("/qdrant/collections/test_collection")

    assert response.status_code == 202
    assert response.json()["message"] == "Collection deleted"


# def test_batch_upload_documents():
#     """Test batch uploading documents to a collection."""
#     # Assuming you have an endpoint for batch uploading documents
#     documents = [
#         {"id": 1, "vector": [0.1, 0.2], "metadata": {"name": "doc1"}},
#         {"id": 2, "vector": [0.3, 0.4], "metadata": {"name": "doc2"}}
#     ]
#     response = client.post(
#         "/documents/batch_upload/",
#         json={"collection_name": "test_collection", "documents": documents}
#     )
#     assert response.status_code == 202
#     assert response.json()["message"] == "Batch upload successful"
