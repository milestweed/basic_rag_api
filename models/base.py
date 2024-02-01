from typing import List, Dict, Union, Tuple
from pydantic import BaseModel

class CollectionList(BaseModel):
    collections: List[str]

