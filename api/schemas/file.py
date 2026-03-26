from pydantic import BaseModel
from typing import List

class FileResponse(BaseModel):
    id: int
    name: str
    size: int
    path: str
    tags: List[str]

class UploadResponse(BaseModel):
    id: int
    name: str
    size: str
    path: str

class DeleteResponse(BaseModel):
    deleted: int

class TagRequest(BaseModel):
    file_ids: List[int]
    tag: str
    action: str  # add / remove
