from fastapi import APIRouter, UploadFile, File
from app.services.owlv2_service import Owlv2Service

router = APIRouter()

@router.post("/")
async def detect_items(file: UploadFile = File(...)):
    """
    Detect clothing items in an uploaded image using Owlv2.
    """
    # This is a placeholder. Owlv2 service implementation will be complex.
    # Service logic should be separated.
    results = Owlv2Service.detect(file)
    return results
