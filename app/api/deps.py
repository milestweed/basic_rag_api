from typing import Generator
from app.services.qdrant import QdrantService
from app.core.config import settings

# Assuming a simple dependency that yields a QdrantService instance
def get_qdrant_service() -> Generator:
    """Dependency that provides access to QdrantService."""
    qdrant_service = QdrantService(
        host=settings.QDRANT_HOST,
        port=settings.QDRANT_PORT
    )
    try:
        yield qdrant_service
    finally:
        qdrant_service.close()  # Assuming the QdrantService class has a close method

# Additional dependencies, such as for authentication or authorization, can be defined here
