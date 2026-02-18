"""
Lumina AI - Visual Commerce Demo
Powered by OWLv2 + SigLIP
"""

import gradio as gr
import torch
import numpy as np
from PIL import Image, ImageDraw
from transformers import Owlv2Processor, Owlv2ForObjectDetection, AutoTokenizer, AutoModel, AutoProcessor

# ===== GLOBAL MODEL CACHE =====
owlv2_processor = None
owlv2_model = None
siglip_processor = None
siglip_model = None

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

def load_owlv2():
    global owlv2_processor, owlv2_model
    if owlv2_processor is None:
        print("Loading OWLv2...")
        owlv2_processor = Owlv2Processor.from_pretrained("google/owlv2-base-patch16-ensemble")
        owlv2_model = Owlv2ForObjectDetection.from_pretrained("google/owlv2-base-patch16-ensemble").to(DEVICE)
        owlv2_model.eval()
        print("OWLv2 loaded!")
    return owlv2_processor, owlv2_model

def load_siglip():
    global siglip_processor, siglip_model
    if siglip_processor is None:
        print("Loading SigLIP...")
        siglip_processor = AutoProcessor.from_pretrained("google/siglip-base-patch16-224")
        siglip_model = AutoModel.from_pretrained("google/siglip-base-patch16-224").to(DEVICE)
        siglip_model.eval()
        print("SigLIP loaded!")
    return siglip_processor, siglip_model


# ===== DETECTION =====
FASHION_LABELS = ["dress", "shirt", "pants", "shoes", "bag", "jacket", "hat", "sunglasses", "skirt", "coat"]

COLORS = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7", "#DDA0DD", "#98D8C8", "#F7DC6F", "#BB8FCE", "#85C1E9"]

def detect_fashion(image):
    if image is None:
        return None, "Please upload an image"
    
    try:
        processor, model = load_owlv2()
        
        image = image.convert("RGB")
        texts = [FASHION_LABELS]
        inputs = processor(text=texts, images=image, return_tensors="pt").to(DEVICE)
        
        with torch.no_grad():
            outputs = model(**inputs)
        
        target_sizes = torch.tensor([image.size[::-1]]).to(DEVICE)
        results = processor.post_process_object_detection(outputs=outputs, target_sizes=target_sizes, threshold=0.1)[0]
        
        draw = ImageDraw.Draw(image)
        detections = []
        
        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            box_coords = [round(i, 1) for i in box.cpu().tolist()]
            label_text = FASHION_LABELS[label]
            conf = round(score.item() * 100, 1)
            color = COLORS[label % len(COLORS)]
            
            draw.rectangle(box_coords, outline=color, width=3)
            draw.rectangle([box_coords[0], box_coords[1]-18, box_coords[0]+len(label_text)*8+40, box_coords[1]], fill=color)
            draw.text((box_coords[0]+4, box_coords[1]-16), f"{label_text} {conf}%", fill="white")
            
            detections.append(f"✅ **{label_text.capitalize()}** — {conf}% confidence")
        
        if not detections:
            return image, "No fashion items detected. Try a clearer outfit photo!"
        
        result_text = f"### 🎯 Detected {len(detections)} item(s)\n\n" + "\n".join(detections)
        return image, result_text
        
    except Exception as e:
        return image, f"Error: {str(e)}"


# ===== VIBE CHECK =====
def vibe_check(image):
    if image is None:
        return "Please upload an image"
    
    try:
        processor, model = load_siglip()
        image = image.convert("RGB")
        
        occasions = ["casual everyday", "formal business", "party night out", "beach vacation", "wedding guest", "gym workout", "date night", "office professional"]
        vibes = ["bohemian free spirit", "minimalist clean", "vintage retro", "streetwear urban", "elegant luxury", "sporty athletic", "edgy punk", "preppy classic"]
        
        all_labels = occasions + vibes
        
        inputs = processor(text=all_labels, images=image, return_tensors="pt", padding="max_length", truncation=True).to(DEVICE)
        
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits_per_image[0]
            probs = torch.softmax(logits, dim=-1).cpu().numpy()
        
        occasion_scores = list(zip(occasions, probs[:len(occasions)]))
        vibe_scores = list(zip(vibes, probs[len(occasions):]))
        
        occasion_scores.sort(key=lambda x: x[1], reverse=True)
        vibe_scores.sort(key=lambda x: x[1], reverse=True)
        
        result = f"""## ✨ Style Analysis

### 🎯 Best Occasion
**{occasion_scores[0][0].title()}** — {occasion_scores[0][1]*100:.0f}% match

### 🎨 Aesthetic Vibe  
**{vibe_scores[0][0].title()}** — {vibe_scores[0][1]*100:.0f}% match

### 📊 All Occasion Scores
"""
        for label, score in occasion_scores[:5]:
            bar = "█" * int(score * 30)
            result += f"\n{label.title()}: {bar} {score*100:.0f}%"
        
        result += "\n\n### 🎭 All Vibe Scores\n"
        for label, score in vibe_scores[:5]:
            bar = "█" * int(score * 30)
            result += f"\n{label.title()}: {bar} {score*100:.0f}%"
        
        return result
        
    except Exception as e:
        return f"Error: {str(e)}"


# ===== SEMANTIC SEARCH =====
SAMPLE_PRODUCTS = [
    {"name": "Red Floral Maxi Dress", "category": "Dresses", "price": 49.99, "style": "bohemian summer dress with floral print"},
    {"name": "Classic Denim Jacket", "category": "Outerwear", "price": 79.99, "style": "blue denim trucker jacket casual"},
    {"name": "White Canvas Sneakers", "category": "Shoes", "price": 59.99, "style": "minimalist white low-top sneakers"},
    {"name": "Black Leather Handbag", "category": "Bags", "price": 129.99, "style": "elegant black crossbody leather bag"},
    {"name": "Gold Aviator Sunglasses", "category": "Accessories", "price": 89.99, "style": "vintage gold frame aviator sunglasses"},
    {"name": "Navy Slim Fit Chinos", "category": "Pants", "price": 44.99, "style": "smart casual navy blue slim pants"},
    {"name": "Silk Blouse Cream", "category": "Tops", "price": 69.99, "style": "elegant cream silk button-up blouse formal"},
    {"name": "Running Shoes Black", "category": "Shoes", "price": 99.99, "style": "sporty black running athletic shoes"},
    {"name": "Wool Overcoat Grey", "category": "Outerwear", "price": 199.99, "style": "formal grey wool long overcoat winter"},
    {"name": "Striped T-Shirt", "category": "Tops", "price": 24.99, "style": "casual blue white striped cotton t-shirt"},
    {"name": "Pleated Midi Skirt", "category": "Skirts", "price": 54.99, "style": "elegant pleated satin midi skirt formal"},
    {"name": "Crossbody Canvas Bag", "category": "Bags", "price": 39.99, "style": "casual canvas crossbody messenger bag"},
]

product_embeddings = None

def get_product_embeddings():
    global product_embeddings
    if product_embeddings is None:
        processor, model = load_siglip()
        texts = [p["style"] for p in SAMPLE_PRODUCTS]
        inputs = processor(text=texts, return_tensors="pt", padding="max_length", truncation=True).to(DEVICE)
        with torch.no_grad():
            text_features = model.get_text_features(**inputs)
            product_embeddings = text_features / text_features.norm(p=2, dim=-1, keepdim=True)
    return product_embeddings

def search_products(query):
    if not query or not query.strip():
        return "Please enter a search query"
    
    try:
        processor, model = load_siglip()
        embeddings = get_product_embeddings()
        
        inputs = processor(text=[query], return_tensors="pt", padding="max_length", truncation=True).to(DEVICE)
        with torch.no_grad():
            query_features = model.get_text_features(**inputs)
            query_features = query_features / query_features.norm(p=2, dim=-1, keepdim=True)
        
        similarities = (query_features @ embeddings.T).squeeze(0).cpu().numpy()
        top_indices = similarities.argsort()[::-1][:5]
        
        result = f"## 🔍 Results for: \"{query}\"\n\n"
        for rank, idx in enumerate(top_indices, 1):
            p = SAMPLE_PRODUCTS[idx]
            score = similarities[idx] * 100
            result += f"""### {rank}. {p['name']}
- **Category**: {p['category']}
- **Price**: ${p['price']}
- **Match**: {score:.1f}%

---
"""
        return result
        
    except Exception as e:
        return f"Error: {str(e)}"


# ===== GRADIO UI =====
css = """
.gradio-container { max-width: 1100px !important; }
h1 { text-align: center; color: #7c3aed; }
"""

with gr.Blocks(title="Lumina AI", css=css, theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🔮 Lumina AI — Visual Commerce Engine")
    gr.Markdown("AI-powered fashion search using **OWLv2** for detection and **SigLIP** for semantic understanding")
    
    with gr.Tabs():
        with gr.Tab("🎯 Detect Items"):
            gr.Markdown("Upload a fashion photo to detect individual items")
            with gr.Row():
                with gr.Column():
                    det_input = gr.Image(type="pil", label="Upload Image")
                    det_btn = gr.Button("Detect Fashion Items", variant="primary", size="lg")
                with gr.Column():
                    det_output_img = gr.Image(label="Detection Results")
                    det_output_text = gr.Markdown()
            det_btn.click(fn=detect_fashion, inputs=det_input, outputs=[det_output_img, det_output_text])
        
        with gr.Tab("✨ Vibe Check"):
            gr.Markdown("Analyze the style, occasion, and aesthetic of an outfit")
            with gr.Row():
                with gr.Column():
                    vibe_input = gr.Image(type="pil", label="Upload Outfit Photo")
                    vibe_btn = gr.Button("Analyze Vibe", variant="primary", size="lg")
                with gr.Column():
                    vibe_output = gr.Markdown()
            vibe_btn.click(fn=vibe_check, inputs=vibe_input, outputs=vibe_output)
        
        with gr.Tab("🔍 Search Products"):
            gr.Markdown("Search our catalog using natural language")
            with gr.Row():
                with gr.Column():
                    search_input = gr.Textbox(label="What are you looking for?", placeholder="e.g., elegant dress for a wedding")
                    gr.Examples(
                        examples=["red summer dress", "casual jacket for weekend", "elegant formal outfit", "sporty running shoes", "vintage style accessories"],
                        inputs=search_input
                    )
                    search_btn = gr.Button("Search", variant="primary", size="lg")
                with gr.Column():
                    search_output = gr.Markdown()
            search_btn.click(fn=search_products, inputs=search_input, outputs=search_output)
    
    gr.Markdown("---")
    gr.Markdown("Built with ❤️ by [Abhi Bhardwaj](https://github.com/AB0204) • [GitHub](https://github.com/AB0204/Lumina-AI)")

if __name__ == "__main__":
    demo.launch()
