from fastapi import APIRouter
from app.api.endpoints import detection, search

api_router = APIRouter()

api_router.include_router(detection.router, prefix="/detect", tags=["detection"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
