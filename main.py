import logging
from fastapi import FastAPI, HTTPException
from modules.db_connection import Qdrant_Connection
from models.base import CollectionList

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

app = FastAPI()
conn = Qdrant_Connection()


@app.get("/")
def root():
    return {"mpathy": "coach"}


@app.get("/create_collection/{name:path}")
async def create_collection(name):
    response = await conn.create_collection(name)
    return response


@app.get("/list_collections/")
async def list_collections() -> CollectionList:
    collections = await conn.list_collections()
    payload = [col.name for col in collections]

    return {"collections": payload}
