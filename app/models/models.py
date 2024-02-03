from typing import List, Optional, Union
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


# Schema for a single document to be uploaded
class Document(BaseModel):
    id: Optional[Union[int, str]] = Field(default=None, description="The unique identifier for the document")
    vector: List[float] = Field(..., description="The encoded vector for the document")
    metadata: Optional[dict] = Field(
        ..., description="Optional metadata for the document"
    )


# Schema for batch uploading documents
class DocumentBatchUpload(BaseModel):
    collection_name: str = Field(
        ..., description="The name of the collection to upload documents to"
    )
    documents: List[Document] = Field(
        ..., description="A list of documents to be uploaded"
    )


# Response model for a successful operation
class OperationStatus(BaseModel):
    message: Optional[str] = Field(
        default=None, description="A message indicating the success or failure of the operation"
    )
    details: Optional[dict] = Field(
        default=None, description="A dictionary of details about the operation"
    )
