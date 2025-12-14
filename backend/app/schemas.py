from pydantic import BaseModel
from typing import Any, Optional, List
from datetime import datetime


class MemoryCreateRequest(BaseModel):
    text: str


class Memory(BaseModel):
    id: str
    text: str
    metadata: dict
    fiboJson: Optional[dict] = None
    imageUrl: Optional[str] = None
    createdAt: datetime


class GenerateJsonRequest(BaseModel):
    id: str


class RenderRequest(BaseModel):
    id: str
