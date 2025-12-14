import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from .schemas import Memory


class MemoryStore:
    def __init__(self) -> None:
        self._memories: List[Memory] = []

    def add(self, text: str, metadata: Dict[str, Any]) -> Memory:
        memory = Memory(
            id=str(uuid.uuid4()),
            text=text,
            metadata=metadata,
            fiboJson=None,
            imageUrl=None,
            createdAt=datetime.utcnow(),
        )
        self._memories.append(memory)
        return memory

    def get_all(self) -> List[Memory]:
        return list(self._memories)

    def get_by_id(self, id: str) -> Optional[Memory]:
        for m in self._memories:
            if m.id == id:
                return m
        return None

    def update(self, id: str, patch: Dict[str, Any]) -> Optional[Memory]:
        for i, m in enumerate(self._memories):
            if m.id == id:
                data = m.model_dump()
                data.update(patch)
                updated = Memory(**data)
                self._memories[i] = updated
                return updated
        return None


memory_store = MemoryStore()
