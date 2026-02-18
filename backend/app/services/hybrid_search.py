"""
Hybrid Search Service
Combines semantic vector search with structured filters.
Real e-commerce search is never pure vector search - it needs
price ranges, categories, stock status, and more.
"""

from typing import List, Optional
from qdrant_client.models import Filter, FieldCondition, MatchValue, Range
from app.services.qdrant_service import QdrantService
from app.core.config import settings


class HybridSearchService:
    """
    Combines:
    - Semantic search (SigLIP embeddings + Qdrant ANN)
    - Structured filters (price, category, stock)
    - Optional reranking (cross-encoder)
    """
    
    @staticmethod
    def build_filter(
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        in_stock: Optional[bool] = None,
        brand: Optional[str] = None,
    ) -> Optional[Filter]:
        """Build Qdrant filter from structured query parameters"""
        conditions = []
        
        if category:
            conditions.append(
                FieldCondition(key="category", match=MatchValue(value=category))
            )
        
        if min_price is not None or max_price is not None:
            price_range = Range(
                gte=min_price if min_price is not None else None,
                lte=max_price if max_price is not None else None,
            )
            conditions.append(
                FieldCondition(key="price", range=price_range)
            )
        
        if in_stock is not None:
            conditions.append(
                FieldCondition(key="in_stock", match=MatchValue(value=in_stock))
            )
        
        if brand:
            conditions.append(
                FieldCondition(key="brand", match=MatchValue(value=brand))
            )
        
        if not conditions:
            return None
        
        return Filter(must=conditions)
    
    @staticmethod
    def search(
        query_embedding: List[float],
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        in_stock: Optional[bool] = None,
        brand: Optional[str] = None,
        limit: int = 20,
    ) -> list:
        """
        Execute hybrid search: vector similarity + structured filters
        
        Example:
            results = HybridSearchService.search(
                query_embedding=embedding,
                category="dress",
                max_price=100.0,
                in_stock=True,
                limit=20
            )
        """
        client = QdrantService.get_client()
        query_filter = HybridSearchService.build_filter(
            category=category,
            min_price=min_price,
            max_price=max_price,
            in_stock=in_stock,
            brand=brand,
        )
        
        results = client.search(
            collection_name=settings.QDRANT_COLLECTION,
            query_vector=query_embedding,
            query_filter=query_filter,
            limit=limit,
        )
        
        return results
