from typing import List, Optional
from pydantic import BaseModel, Field


# Schema for creating a new collection
class Collection(BaseModel):
    name: str = Field(..., description="The name of the collection")

class CollectionCreate(Collection):
    dimensions: str = Field(
        default=2048, description="The dimension size. Default: 2048"
    )
    distance: str = Field(
        default="cosine", description="The similarity metric used. Default: cosine"
    )


# Assuming a simple Vector model for demonstration
class VectorModel(BaseModel):
    id: str
    vector: List[float]
    metadata: Optional[dict] = None


# Schema for a single document to be uploaded
class Document(BaseModel):
    id: int = Field(..., description="The unique identifier for the document")
    vector: List[float] = Field(..., description="The encoded vector for the document")
    metadata: Optional[dict] = Field(
        None, description="Optional metadata for the document"
    )


# Schema for batch uploading documents
class DocumentBatchUpload(BaseModel):
    collection_name: str = Field(
        ..., description="The name of the collection to upload documents to"
    )
    documents: List[Document] = Field(
        ..., description="A list of documents to be uploaded"
    )


# Example response model for a successful operation
class OperationStatus(BaseModel):
    message: Optional[str] = Field(
        ..., description="A message indicating the success or failure of the operation"
    )
    details: Optional[dict] = Field(
        ..., description="A dictionary of details about the operation"
    )


class VectorBase(BaseModel):
    vector: List[float] = Field(
        ..., description="The vector representation of the document"
    )
    metadata: Optional[dict] = Field(
        None, description="Optional metadata associated with the document"
    )


class VectorCreate(VectorBase):
    collection_name: str


class VectorUpdate(BaseModel):
    vector: Optional[List[float]] = Field(
        None, description="The new vector representation, if updating"
    )
    metadata: Optional[dict] = Field(
        None, description="New or updated metadata for the document"
    )
