"""
Lumina AI - Gradio Demo
A visual commerce engine with semantic fashion search
"""

import gradio as gr
import torch
from PIL import Image, ImageDraw, ImageFont
from transformers import Owlv2Processor, Owlv2ForObjectDetection, SiglipProcessor, SiglipModel
import numpy as np
from typing import List, Tuple, Dict
import json

# ===== MODEL INITIALIZATION =====
class ModelCache:
    """Singleton pattern for model caching"""
    _owlv2_processor = None
    _owlv2_model = None
    _siglip_processor = None
    _siglip_model = None
    _product_embeddings = None
    _product_data = None
    
    @classmethod
    def get_owlv2(cls):
        if cls._owlv2_processor is None:
            print("Loading OWLv2...")
            cls._owlv2_processor = Owlv2Processor.from_pretrained("google/owlv2-base-patch16-ensemble")
            cls._owlv2_model = Owlv2ForObjectDetection.from_pretrained("google/owlv2-base-patch16-ensemble")
            cls._owlv2_model.eval()
            if torch.cuda.is_available():
                cls._owlv2_model = cls._owlv2_model.cuda()
        return cls._owlv2_processor, cls._owlv2_model
    
    @classmethod
    def get_siglip(cls):
        if cls._siglip_processor is None:
            print("Loading SigLIP...")
            cls._siglip_processor = SiglipProcessor.from_pretrained("google/siglip-base-patch16-384")
            cls._siglip_model = SiglipModel.from_pretrained("google/siglip-base-patch16-384")
            cls._siglip_model.eval()
            if torch.cuda.is_available():
                cls._siglip_model = cls._siglip_model.cuda()
        return cls._siglip_processor, cls._siglip_model
    
    @classmethod
    def load_products(cls):
        """Load pre-computed product embeddings and metadata"""
        if cls._product_data is None:
            # Sample dataset (in production, load from file)
            cls._product_data = [
                {"title": "Red Floral Summer Dress", "price": 49.99, "category": "Dresses", "url": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400"},
                {"title": "Classic Denim Jacket", "price": 79.99, "category": "Jackets", "url": "https://images.unsplash.com/photo-1576995853123-5a10305d93c0?w=400"},
                {"title": "White Sneakers", "price": 89.99, "category": "Shoes", "url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400"},
                {"title": "Leather Crossbody Bag", "price": 129.99, "category": "Bags", "url": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=400"},
                {"title": "Black Sunglasses", "price": 149.99, "category": "Accessories", "url": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400"},
            ]
            # Precompute embeddings
            cls._product_embeddings = cls._compute_embeddings()
        return cls._product_data, cls._product_embeddings
    
    @classmethod
    def _compute_embeddings(cls):
        """Compute embeddings for all products"""
        processor, model = cls.get_siglip()
        embeddings = []
        
        for product in cls._product_data:
            # In production, use actual product images
            # For demo, use text embeddings
            inputs = processor(text=[product["title"]], return_tensors="pt", padding="max_length")
            if torch.cuda.is_available():
                inputs = {k: v.cuda() for k, v in inputs.items()}
            
            with torch.no_grad():
                text_features = model.get_text_features(**inputs)
                text_features = text_features / text_features.norm(p=2, dim=-1, keepdim=True)
            
            embeddings.append(text_features.cpu().numpy()[0])
        
        return np.array(embeddings)


# ===== DETECTION FUNCTION =====
def detect_objects(image: Image.Image) -> Tuple[Image.Image, str]:
    """Detect fashion items in image and draw bounding boxes"""
    processor, model = ModelCache.get_owlv2()
    
    # Fashion categories
    texts = [["dress", "shirt", "pants", "shoes", "bag", "jacket", "hat", "sunglasses", "watch"]]
    
    inputs = processor(text=texts, images=image, return_tensors="pt")
    if torch.cuda.is_available():
        inputs = {k: v.cuda() for k, v in inputs.items()}
    
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Post-process
    target_sizes = torch.tensor([image.size[::-1]])
    results = processor.post_process_object_detection(outputs=outputs, target_sizes=target_sizes, threshold=0.1)[0]
    
    # Draw bounding boxes
    draw = ImageDraw.Draw(image)
    detections_text = []
    
    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        box = [round(i, 2) for i in box.tolist()]
        label_text = texts[0][label]
        confidence = round(score.item(), 2)
        
        # Draw box
        draw.rectangle(box, outline="red", width=3)
        draw.text((box[0], box[1]-10), f"{label_text} ({confidence})", fill="red")
        
        detections_text.append(f"✅ {label_text.capitalize()} - {confidence*100:.0f}% confidence")
    
    result_text = "\n".join(detections_text) if detections_text else "No items detected. Try a fashion image!"
    
    return image, result_text


# ===== VIBE CHECK FUNCTION =====
def vibe_check(image: Image.Image) -> str:
    """Analyze style, occasion, and vibe of the image"""
    processor, model = ModelCache.get_siglip()
    
    # Style categories
    occasions = ["casual", "formal", "party", "beach", "wedding", "office", "gym", "date night"]
    vibes = ["bohemian", "minimalist", "vintage", "streetwear", "elegant", "sporty", "edgy"]
    
    # Compute image embedding
    inputs = processor(images=image, return_tensors="pt")
    if torch.cuda.is_available():
        inputs = {k: v.cuda() for k, v in inputs.items()}
    
    with torch.no_grad():
        image_features = model.get_image_features(**inputs)
        image_features = image_features / image_features.norm(p=2, dim=-1, keepdim=True)
    
    # Compare with text categories
    text_inputs = processor(text=occasions + vibes, return_tensors="pt", padding="max_length")
    if torch.cuda.is_available():
        text_inputs = {k: v.cuda() for k, v in text_inputs.items()}
    
    with torch.no_grad():
        text_features = model.get_text_features(**text_inputs)
        text_features = text_features / text_features.norm(p=2, dim=-1, keepdim=True)
    
    # Compute similarities
    similarities = (image_features @ text_features.T).cpu().numpy()[0]
    
    # Get top matches
    top_occasion_idx = similarities[:len(occasions)].argmax()
    top_vibe_idx = len(occasions) + similarities[len(occasions):].argmax()
    
    result = f"""
🎯 **Style Analysis**

**Occasion**: {occasions[top_occasion_idx].capitalize()} ({similarities[top_occasion_idx]*100:.0f}%)
**Vibe**: {vibes[top_vibe_idx - len(occasions)].capitalize()} ({similarities[top_vibe_idx]*100:.0f}%)

**Other Matches**:
"""
    # Add top 3 matches
    sorted_idx = similarities.argsort()[::-1][:5]
    for idx in sorted_idx:
        if idx < len(occasions):
            result += f"\n- {occasions[idx].capitalize()}: {similarities[idx]*100:.0f}%"
        else:
            result += f"\n- {vibes[idx - len(occasions)].capitalize()}: {similarities[idx]*100:.0f}%"
    
    return result


# ===== SEARCH FUNCTION =====
def semantic_search(query: str, top_k: int = 5) -> str:
    """Search products by text query"""
    processor, model = ModelCache.get_siglip()
    product_data, product_embeddings = ModelCache.load_products()
    
    # Compute query embedding
    inputs = processor(text=[query], return_tensors="pt", padding="max_length")
    if torch.cuda.is_available():
        inputs = {k: v.cuda() for k, v in inputs.items()}
    
    with torch.no_grad():
        query_features = model.get_text_features(**inputs)
        query_features = query_features / query_features.norm(p=2, dim=-1, keepdim=True)
    
    # Compute similarities
    query_embedding = query_features.cpu().numpy()[0]
    similarities = np.dot(product_embeddings, query_embedding)
    
    # Get top results
    top_indices = similarities.argsort()[::-1][:top_k]
    
    result = f"### 🔍 Search Results for: \"{query}\"\n\n"
    for idx in top_indices:
        product = product_data[idx]
        score = similarities[idx]
        result += f"""
**{product['title']}**
- Price: ${product['price']}
- Category: {product['category']}
- Similarity: {score*100:.1f}%
- [View Product]({product['url']})

---
"""
    
    return result


# ===== GRADIO INTERFACE =====
with gr.Blocks(title="Lumina AI - Visual Search Demo", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🔮 Lumina AI - Visual Commerce Engine
    ### AI-powered fashion search using OWLv2, SigLIP, and semantic embeddings
    """)
    
    with gr.Tabs():
        # Tab 1: Object Detection
        with gr.Tab("🎯 Object Detection"):
            gr.Markdown("Upload a fashion image to detect items with bounding boxes")
            with gr.Row():
                with gr.Column():
                    detect_input = gr.Image(type="pil", label="Upload Image")
                    detect_btn = gr.Button("Detect Items", variant="primary")
                with gr.Column():
                    detect_output_img = gr.Image(label="Detected Objects")
                    detect_output_text = gr.Textbox(label="Detection Results", lines=10)
            
            detect_btn.click(fn=detect_objects, inputs=detect_input, outputs=[detect_output_img, detect_output_text])
        
        # Tab 2: Vibe Check
        with gr.Tab("✨ Vibe Check"):
            gr.Markdown("Analyze the style, occasion, and aesthetic of an outfit")
            with gr.Row():
                with gr.Column():
                    vibe_input = gr.Image(type="pil", label="Upload Image")
                    vibe_btn = gr.Button("Analyze Vibe", variant="primary")
                with gr.Column():
                    vibe_output = gr.Markdown(label="Style Analysis")
            
            vibe_btn.click(fn=vibe_check, inputs=vibe_input, outputs=vibe_output)
        
        # Tab 3: Semantic Search
        with gr.Tab("🔍 Semantic Search"):
            gr.Markdown("Search for products using natural language")
            with gr.Row():
                with gr.Column():
                    search_input = gr.Textbox(label="Search Query", placeholder="e.g., 'red dress for summer party'")
                    search_examples = gr.Examples(
                        examples=["red dress for beach wedding", "casual denim jacket", "elegant black handbag"],
                        inputs=search_input
                    )
                    search_btn = gr.Button("Search", variant="primary")
                with gr.Column():
                    search_output = gr.Markdown(label="Search Results")
            
            search_btn.click(fn=semantic_search, inputs=search_input, outputs=search_output)
    
    gr.Markdown("""
    ---
    **Built with** [OWLv2](https://huggingface.co/google/owlv2-base-patch16-ensemble) • 
    [SigLIP](https://huggingface.co/google/siglip-base-patch16-384) • 
    [Gradio](https://gradio.app)
    
    [GitHub](https://github.com/AB0204/Lumina-AI) • [Documentation](https://github.com/AB0204/Lumina-AI/blob/main/README.md)
    """)

if __name__ == "__main__":
    demo.launch()
