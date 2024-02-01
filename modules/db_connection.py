import logging
from typing import List

from fastapi import status, responses
from qdrant_client import QdrantClient
from qdrant_client.http import models

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)


class Qdrant_Connection:
    def __init__(self):
        self.client = QdrantClient(location="http://localhost/", port=6333)

    def list_collections(self) -> List:
        response = self.client.get_collections()
        
        return response.collections

    def create_collection(
        self,
        name: str,
        vector_size: int = 2048,
        sim_metric: models.Distance = models.Distance.COSINE,
    ) -> None:
        try:
            response = self.client.create_collection(
                collection_name=name,
                vectors_config=models.VectorParams(
                    size=vector_size, distance=sim_metric
                ),
            )
            print(response)
            logger.info(
                "Collection created!\n\tName: %s\n\tVector size: %i"
                % (name, vector_size)
            )
            return None
        except Exception as e:
            logger.warning(
                "Collection creation failed!\n\tName: %s\n\tVector size: %i"
                % (name, vector_size))
            return e

    def delete_collection(self, name: str) -> None:
        self.client.delete_collection(name)

        return {}

    def upload_vectors(self):
        pass


if __name__ == "__main__":
    conn = Qdrant_Connection()

    print(conn.list_collections())
