import os
import json
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    # Qdrant database configurations
    QDRANT_HOST: str = os.environ['QDRANT_HOST']
    QDRANT_PORT: int = os.environ['QDRANT_PORT']
    QDRANT_API_KEY: str = os.environ['QDRANT_API_KEY']

    # Application configurations
    APP_NAME: str = os.environ['APP_NAME']
    APP_VERSION: str = os.environ['APP_VERSION']
    APP_DESCRIPTION: str = os.environ['APP_DESCRIPTION']

    # CORS settings for FastAPI
    # ["*"] to accept all origins
    CORS_ORIGINS: list = json.loads(os.environ['CORS_ORIGINS'])


settings = Settings()
