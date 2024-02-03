from fastapi import APIRouter, HTTPException, Path, Body
from typing import List, Dict, Union, Annotated
from app.models.models import (
    Collection,
    CollectionCreate,
    Document,
    OperationStatus,
)
from app.services.qdrant import QdrantService

router = APIRouter()
qdrant_service = QdrantService()


@router.post("/collections/", status_code=201, response_model=OperationStatus)
async def create_collection(collection: CollectionCreate):
    """
    Create a new collection in the Qdrant database.
    """
    response = await qdrant_service.create_collection(collection_data=collection)
    if not response["success"]:
        raise HTTPException(
            status_code=response["status_code"], detail=response["content"]
        )
    return OperationStatus(
        message="Collection created successfully",
        details={
            "name": collection.name,
            "dimensions": collection.dimensions,
            "distance": collection.distance,
        },
    )


@router.get("/collections/", status_code=200, response_model=OperationStatus)
async def get_collections():
    """List the collection in the database

    Raises:
        HTTPException: Information describing why the collection could not be retrieved
    Returns:
        OperationStatus: A list of the collections within the database
    """
    response = await qdrant_service.list_collections()
    if not response["success"]:
        raise HTTPException(status_code=400, detail=response["content"])
    return OperationStatus(
        message="Collections found", details={"collections": response["content"]}
    )


@router.get(
    "/collections/{collection_name}", status_code=200, response_model=OperationStatus
)
async def get_collection_info(
    collection_name: Annotated[str, Path(title="The name of a collection that exist.")]
):
    """Returns information about a collection within the database

    Args:
        collection_name (str): The name of a collection that exist.

    Raises:
        HTTPException: Collection not found

    Returns:
        dict: A json of the parameters associated with the given collection.
    """
    response = await qdrant_service.get_collection_info(
        Collection(name=collection_name)
    )
    if not response["success"]:
        raise HTTPException(
            status_code=response["status_code"], detail=response["content"]
        )
    return OperationStatus(message="Collection found", details=response["content"])


@router.delete(
    "/collections/{collection_name}", status_code=202, response_model=OperationStatus
)
async def delete_collection(
    collection_name: Annotated[
        str, Path(title="The name of an existing collection to delete.")
    ]
):
    """Deletes a collection that exists within the database

    Raises:
        HTTPException: Collection not found

    Returns:
        OperationStatus: Collection Deleted
    """
    collection_data = Collection(name=collection_name)
    success = await qdrant_service.delete_collection(collection_data=collection_data)
    if not success:
        raise HTTPException(status_code=400, detail="Collection not found.")
    return OperationStatus(message="Collection deleted", details=None)


@router.post("/", status_code=201, response_model=OperationStatus)
async def upload_document(document: Document, collection_name: str):
    """
    Upload a document to the qdrant database.
    """
    c = Collection(name=collection_name)
    response = await qdrant_service.upload_document(collection=c, document=document)
    if not response["success"]:
        raise HTTPException(
            status_code=response["status_code"], detail=response["content"]
        )
    return OperationStatus(message="Document uploaded", details=response["content"])
