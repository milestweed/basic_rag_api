from typing import List, Dict
import logging
import json
from fastapi import HTTPException
from app.core.config import settings
from app.models.models import Collection, CollectionCreate, Document
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
            logger.warning(f"Could not retrieve collections: {e}")
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
            logger.warning(f"Could not retrieve collection: {e.__dict__}")
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

    async def upload_document(self, collection: Collection, document: Document) -> Dict:

        try:
            response = self.client.upsert(
                collection_name=collection.name,
                points=[
                    models.PointStruct(
                        id=document.id,
                        vector=document.vector,
                        payload=document.metadata,
                    )
                ],
            )
            return {"success": True, "content": json.loads(response.model_dump_json())}
        except Exception as e:
            content = e.__dict__
            status_info = content
            logger.warning(f"Could not add document: {content}")
            return {
                "success": False,
                "status_code": 400,
                "content": status_info,
            }

    async def get_document(self, collection: Collection, document: Document) -> Dict:
        try:
            response = self.client.retrieve(
                collection_name=collection.name,
                ids=[document.id],
                with_vectors=True,
            )
            return {"success": True, "content": json.loads(response[0].model_dump_json())}
        except Exception as e:
            logger.warning(f"Could not get document: {e}")
            return {
                "success": False,
                "status_code": 400,
                "content": e,
            }

    async def update_document(self, collection: Collection, document: Document) -> Dict:
        try:
            response = self.client.update_vectors(
                collection_name=collection.name,
                points=[models.PointVectors(id=document.id, vector=document.vector)]
            )
            return {"success": True, "content": json.loads(response.model_dump_json())}
        except Exception as e:
            logger.warning(f"Could not update document: {e}")
            return {
                "success": False,
                "status_code": 400,
                "content": str(e),
            }

    async def delete_document(self, collection: Collection, document: Document) -> Dict:
        try:
            response = self.client.delete(
                collection_name=collection.name,
                points_selector=models.PointIdsList(points=[document.id]),
            )
            return {"success": True, "content": json.loads(response.model_dump_json())}
        except Exception as e:
            content = e.__dict__
            logger.warning(content)
            status_info = content
            logger.warning(f"Could not delete document: {content}")
            return {
                "success": False,
                "status_code": 400,
                "content": status_info,
            }
