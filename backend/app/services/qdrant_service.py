from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from app.core.config import settings
import uuid

class QdrantService:
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            cls._client = QdrantClient(url=settings.QDRANT_URL)
        return cls._client

    @staticmethod
    def init_collection():
        client = QdrantService.get_client()
        if not client.collection_exists(settings.QDRANT_COLLECTION):
            client.create_collection(
                collection_name=settings.QDRANT_COLLECTION,
                # SigLIP vector size = 1152
                vectors_config=VectorParams(size=1152, distance=Distance.COSINE),
            )
            print(f"Collection '{settings.QDRANT_COLLECTION}' created.")

    @staticmethod
    def upsert_item(embedding: list[float], payload: dict):
        client = QdrantService.get_client()
        point_id = str(uuid.uuid4())
        
        client.upsert(
            collection_name=settings.QDRANT_COLLECTION,
            points=[
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=payload
                )
            ]
        )
        return point_id

    @staticmethod
    def search(embedding: list[float], limit: int = 5):
        client = QdrantService.get_client()
        results = client.search(
            collection_name=settings.QDRANT_COLLECTION,
            query_vector=embedding,
            limit=limit
        )
        return results
