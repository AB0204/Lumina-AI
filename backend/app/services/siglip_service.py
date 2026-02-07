import torch
from transformers import SiglipProcessor, SiglipModel
from PIL import Image
import io
from app.core.config import settings

class SiglipService:
    _processor = None
    _model = None

    @classmethod
    def get_model(cls):
        if cls._model is None:
            print(f"Loading SigLIP model: {settings.SIGLIP_MODEL_ID}...")
            cls._processor = SiglipProcessor.from_pretrained(settings.SIGLIP_MODEL_ID)
            cls._model = SiglipModel.from_pretrained(settings.SIGLIP_MODEL_ID)
            cls._model.eval()
        return cls._processor, cls._model

    @staticmethod
    def get_embedding(image_bytes: bytes):
        processor, model = SiglipService.get_model()
        try:
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        except Exception:
            raise ValueError("Invalid image")

        inputs = processor(images=image, return_tensors="pt")
        with torch.no_grad():
            outputs = model.get_image_features(**inputs)
            # Normalize embedding
            embedding = outputs / outputs.norm(p=2, dim=-1, keepdim=True)
            
        return embedding[0].tolist()

    @staticmethod
    def get_text_embedding(text: str):
        processor, model = SiglipService.get_model()
        inputs = processor(text=[text], return_tensors="pt", padding="max_length")
        with torch.no_grad():
            outputs = model.get_text_features(**inputs)
            embedding = outputs / outputs.norm(p=2, dim=-1, keepdim=True)
            
        return embedding[0].tolist()
