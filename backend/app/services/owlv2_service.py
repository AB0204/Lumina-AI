from PIL import Image
import torch
from transformers import Owlv2Processor, Owlv2ForObjectDetection
from app.core.config import settings
import io

class Owlv2Service:
    _processor = None
    _model = None

    @classmethod
    def get_model(cls):
        if cls._model is None:
            print(f"Loading Owlv2 model: {settings.OWLV2_MODEL_ID}...")
            cls._processor = Owlv2Processor.from_pretrained(settings.OWLV2_MODEL_ID)
            cls._model = Owlv2ForObjectDetection.from_pretrained(settings.OWLV2_MODEL_ID)
            cls._model.eval()
            print("Model loaded successfully.")
        return cls._processor, cls._model

    @staticmethod
    def detect(image_bytes: bytes, texts: list[str] = None):
        if texts is None:
            # Default fashion labels for "Magic Crop"
            texts = ["shirt", "pants", "dress", "sunglasses", "shoes", "bag", "jacket", "hat", "watch", "skirt"]

        processor, model = Owlv2Service.get_model()

        try:
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        except Exception as e:
            raise ValueError(f"Invalid image format: {e}")

        # Owlv2 expects text queries as a list of lists (one list per image)
        inputs = processor(text=[texts], images=image, return_tensors="pt")

        with torch.no_grad():
            outputs = model(**inputs)

        # Target image size for post-processing
        target_sizes = torch.tensor([image.size[::-1]])
        
        # Post-process outputs to get bounding boxes (normalized 0-1 or absolute)
        # Using threshold from settings
        results = processor.post_process_object_detection(
            outputs=outputs, 
            target_sizes=target_sizes, 
            threshold=settings.CONFIDENCE_THRESHOLD
        )[0]

        detections = []
        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            box = [round(i, 2) for i in box.tolist()]
            detections.append({
                "label": texts[label],
                "confidence": round(score.item(), 2),
                "box": box  # [xmin, ymin, xmax, ymax]
            })

        return {
            "detections": detections,
            "count": len(detections)
        }
