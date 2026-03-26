from pydantic import BaseModel
from typing import List

class FileResponse(BaseModel):
    id: int
    name: str
    size: int
    path: str
    tags: List[str]
