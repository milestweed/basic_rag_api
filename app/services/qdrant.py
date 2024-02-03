from typing import List, Dict
import logging
import json
from fastapi import HTTPException
from app.core.config import settings
from app.models.models import Collection, CollectionCreate, DocumentBatchUpload
from qdrant_client import QdrantClient
from qdrant_client.http import models

logger = logging.getLogger("uvicorn")


class QdrantService:
    def __init__(self):
        # Initialize Qdrant client
        self.client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT,
        )
        self.distance = {
            "cosine": models.Distance.COSINE,
            "dot": models.Distance.DOT,
            "euclid": models.Distance.EUCLID,
            "manhattan": models.Distance.MANHATTAN,
        }

    async def create_collection(self, collection_data: CollectionCreate) -> Dict:
        """
        Creates a new collection in Qdrant using the provided collection data.
        """
        if collection_data.distance not in self.distance.keys():
            logger.warning(f"Could not create collection '{collection_data.name}'.")
            logger.warning(f"Improper distance signifier '{collection_data.distance}'.")
            logger.info(
                "Distance must be one of ['cosine', 'dot', 'euclid', 'manhattan']."
            )
            return {
                "success": False,
                "status_code": 400,
                "content": {
                    "status": {
                        "error": f"Improper distance signifier '{collection_data.distance}'.",
                        "reason": "Distance must be one of ['cosine', 'dot', 'euclid', 'manhattan'].",
                    }
                },
            }
        try:
            self.client.create_collection(
                collection_name=collection_data.name,
                vectors_config=models.VectorParams(
                    size=collection_data.dimensions,
                    distance=self.distance[collection_data.distance],
                ),
            )
            logger.info(f"Collection {collection_data.name} successfully created!")
            return {"success": True}
        except Exception as e:
            content = e.__dict__
            status_code = content["status_code"]
            status_info = json.loads(content["content"])
            logger.warning(f"Could not retrieve collection: {e.__dict__}")
            return {
                "success": False,
                "status_code": status_code,
                "content": status_info,
            }

    async def list_collections(self) -> Dict:
        """Lists all collections in the Qdrant database

        Returns:
            dict: A dictionary containing the status of the operation and
                a list of collection names in the database if the operation was
                successful.
        """
        try:
            response = self.client.get_collections()
            collections = [c.name for c in response.collections]
            return {"success": True, "content": collections}

        except Exception as e:
            logger.warn(f"Could not retrieve collections: {e}")
            return {"success": False, "content": e}

    async def get_collection_info(self, collection_data: Collection) -> Dict:
        """Lists details about a collection in the Qdrant database

        Returns:
            dict: A dictionary containing the status of the operation and
                a dictionary of collection details if the operation was
                successful.
        """
        try:
            response = self.client.get_collection(collection_data.name)
            info = json.loads(response.model_dump_json())
            return {"success": True, "content": info}

        except Exception as e:
            content = e.__dict__
            status_code = content["status_code"]
            status_info = json.loads(content["content"])
            logger.warn(f"Could not retrieve collection: {e.__dict__}")
            return {
                "success": False,
                "status_code": status_code,
                "content": status_info,
            }

    async def delete_collection(self, collection_data: Collection) -> Dict:
        """Removes a collection in the Qdrant database

        Returns:
            dict: A dictionary containing the status of the operation and
                any details.
        """
        success = self.client.delete_collection(collection_data.name)
        return success

    ###############################################
    ##                     TODO                  ##
    ###############################################

    async def batch_upload_documents(self, batch_data: DocumentBatchUpload) -> bool:
        """
        Uploads a batch of documents to a specified collection in Qdrant.
        """
        try:
            # Assuming `QdrantClient` has a method for batch uploads
            # Convert `DocumentBatchUpload` schema to the format expected by Qdrant if necessary
            self.client.upsert(
                collection_name=batch_data.collection_name,
                documents=batch_data.documents,
            )
            return True
        except Exception as e:
            # Log the error or handle it as needed
            print(f"Error in batch uploading documents: {e}")
            return False

    async def create_document(self):
        pass

    async def get_document(self):
        pass

    async def update_document(self):
        pass

    async def delete_document(self, document_id: int, collection_name: str) -> bool:
        """
        Deletes a Document from the Qdrant database by its ID.

        Args:
            vector_id (int): The ID of the vector to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        try:
            # Assuming `delete` is an async method of the client
            # Adjust the method call according to your client's API
            response = self.client.delete(
                collection_name=collection_name, document_id=document_id
            )
            if (
                response.is_success
            ):  # Check success based on your client's response structure
                return True
            else:
                return False
        except Exception as e:
            # Log the exception or handle it as needed
            raise HTTPException(
                status_code=500, detail=f"Error deleting vector: {str(e)}"
            )