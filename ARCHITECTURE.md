# System Architecture

```mermaid
graph TB
    User[User Query] --> API[API Gateway / FastAPI]
    
    API --> Cache{Redis Cache}
    Cache -->|Cache Hit| Return[Return Results]
    Cache -->|Cache Miss| ML[ML Pipeline]
    
    ML --> Detection[OWLv2 Detection]
    ML --> Embedding[SigLIP Embeddings]
    
    Detection --> Crop[Cropped Images]
    Embedding --> Vector[Vector Search]
    
    Crop --> Vector
    Vector --> Qdrant[(Qdrant Vector DB)]
    
    Qdrant --> Rank[Ranked Results]
    Rank --> Return
    
    style API fill:#9333ea
    style Cache fill:#f59e0b
    style Qdrant fill:#3b82f6
    style Return fill:#10b981
```

## Components

- **FastAPI**: High-performance async API gateway
- **Redis**: Query result caching (1hr TTL)
- **OWLv2**: Zero-shot object detection
- **SigLIP**: Multimodal embeddings (1152-dim)
- **Qdrant**: Vector similarity search (Cosine)
