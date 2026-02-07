from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.owlv2_service import Owlv2Service
from typing import List, Optional
import io

router = APIRouter()

@router.post("/")
async def detect_apparel(
    file: UploadFile = File(...),
    labels: Optional[List[str]] = None
):
    """
    Zero-Shot Detection of Fashion Items.
    Upload an image -> Get bounding boxes for 'shirt', 'dress', 'shoes', etc.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        content = await file.read()
        results = Owlv2Service.detect(content, labels)
        return {
            "status": "success",
            "meta": {
                "filename": file.filename,
                "model": "Owlv2-Ensemble"
            },
            "data": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
