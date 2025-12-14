import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from .schemas import MemoryCreateRequest, Memory, GenerateJsonRequest, RenderRequest
from .store import memory_store
from .services.llm_service import parse_memory_to_metadata
from .services.fibo_service import (
    build_fibo_json_from_metadata,
    render_with_fibo,
    translate_with_fibo,
)

load_dotenv()

app = FastAPI(title="Memories Reimagined API")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"status": "ok", "message": "Memories Reimagined backend is running"}


@app.get("/api/memories", response_model=list[Memory])
async def list_memories():
    return memory_store.get_all()


@app.post("/api/memories/parse", response_model=Memory)
async def parse_memory(req: MemoryCreateRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="text is required")

    metadata = await parse_memory_to_metadata(req.text)
    memory = memory_store.add(text=req.text, metadata=metadata)
    return memory


@app.post("/api/memories/generate-json")
async def generate_json(req: GenerateJsonRequest):
    """
    1) Take the stored memory text
    2) Ask FIBO translator to turn it into a structured prompt
    3) Combine that with our emotional metadata
    4) Save as memory.fiboJson
    """
    memory = memory_store.get_by_id(req.id)
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")

    # Call FIBO translator (or fallback if FIBO_TRANSLATE_URL not set)
    structured = await translate_with_fibo(memory.text)

    # Merge our metadata with FIBO's structured prompt
    fibo_json = build_fibo_json_from_metadata(memory.metadata, structured)
    updated = memory_store.update(req.id, {"fiboJson": fibo_json})
    return {"id": updated.id, "fiboJson": updated.fiboJson}


@app.post("/api/memories/render")
async def render_memory(req: RenderRequest):
    memory = memory_store.get_by_id(req.id)
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")

    if not memory.fiboJson:
        raise HTTPException(
            status_code=400, detail="No FIBO JSON exists for this memory yet"
        )

    image_url = await render_with_fibo(memory.fiboJson)
    updated = memory_store.update(req.id, {"imageUrl": image_url})
    return {"id": updated.id, "imageUrl": updated.imageUrl}
