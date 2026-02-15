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

import hashlib
from app.services.redis_service import RedisService

# ... imports ...

@router.post("/", response_model=List[SearchResponse])
async def search_items(query: SearchQuery):
    """
    Multimodal Semantic Search with Redis Caching:
    1. Check Redis cache for query hash.
    2. If hit, return cached results.
    3. If miss, generate embedding -> search Qdrant -> cache results.
    """
    if not query.query_text:
        return []

    # Generate cache key
    query_hash = hashlib.md5(f"{query.query_text}-{query.top_k}".encode()).hexdigest()
    cache_key = f"search:{query_hash}"

    # 1. Check Cache
    cached_results = await RedisService.get_cache(cache_key)
    if cached_results:
        return cached_results

    # 2. Generate text embedding
    embedding = SiglipService.get_text_embedding(query.query_text)
    
    # 3. Search in Vector DB
    results = QdrantService.search(embedding, limit=query.top_k)
    
    # 4. Format response
    response = []
    for hit in results:
        response.append({
            "score": hit.score,
            "payload": hit.payload
        })
    
    # 5. Set Cache (TTL: 1 hour)
    await RedisService.set_cache(cache_key, response, expire=3600)
        
    return response

@router.on_event("startup")
async def startup_event():
    # Ensure collection exists on startup
    QdrantService.init_collection()
