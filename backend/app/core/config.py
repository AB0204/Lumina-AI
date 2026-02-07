from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Lumina API"
    
    # Model Configuration
    OWLV2_MODEL_ID: str = "google/owlv2-base-patch16-ensemble"
    SIGLIP_MODEL_ID: str = "google/siglip-so400m-patch14-384"
    CONFIDENCE_THRESHOLD: float = 0.15

    # Database
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_COLLECTION: str = "lumina_products_v1"
    
    # Infrastructure
    REDIS_URL: str = "redis://localhost:6379"

    class Config:
        env_file = ".env"

settings = Settings()
