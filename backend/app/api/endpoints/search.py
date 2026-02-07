from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from app.services.siglip_service import SiglipService
from app.services.qdrant_service import QdrantService

router = APIRouter()

class SearchQuery(BaseModel):
    query_text: Optional[str] = None
    top_k: int = 5

class SearchResponse(BaseModel):
    score: float
    payload: dict

@router.post("/", response_model=List[SearchResponse])
async def search_items(query: SearchQuery):
    """
    Multimodal Semantic Search:
    Takes a text description -> Generates SigLIP embedding -> Searches Qdrant.
    Example: "red dress for a wedding"
    """
    if not query.query_text:
        return []

    # 1. Generate text embedding
    embedding = SiglipService.get_text_embedding(query.query_text)
    
    # 2. Search in Vector DB
    results = QdrantService.search(embedding, limit=query.top_k)
    
    # 3. Format response
    response = []
    for hit in results:
        response.append({
            "score": hit.score,
            "payload": hit.payload
        })
        
    return response

@router.on_event("startup")
async def startup_event():
    # Ensure collection exists on startup
    QdrantService.init_collection()
