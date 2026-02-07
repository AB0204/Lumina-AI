from fastapi import FastAPI
from app.api.api_router import api_router
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Intelligent Visual Commerce Engine powered by Owlv2 & SigLIP",
    version="0.1.0",
    docs_url="/docs",
    redoc_url=None,
)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def health_check():
    return {
        "service": "Lumina API",
        "status": "active",
        "version": "0.1.0"
    }
