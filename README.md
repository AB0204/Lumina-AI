# Lumina - The AI-Powered Style Engine

Lumina is an intelligent visual commerce backend that understands fashion not just by keywords, but by *style, vibe, and visual similarity*. It leverages state-of-the-art computer vision models (Owlv2, SigLIP) to power next-generation e-commerce search.

## 🚀 The Vision
Traditional search: "Red dress" -> Returns 10,000 red dresses.
**Lumina Search**: "Find me a dress with this *bohemian vibe* but for a *formal wedding*" -> Returns the perfect match.

## 🛠️ The Tech Stack
*   **Core AI**:
    *   **Qwen-VL**: For high-level scene understanding and tagging (e.g., "Park", "Casual", "Summer").
    *   **Owlv2**: Zero-Shot Object Detection (detects "shirt", "dress", "shoes" with high precision).
    *   **SigLIP**: Multimodal Embeddings for vector search (matching text description to image content).
*   **Backend**: FastAPI (Python) - Async, high-performance API.
*   **Database**: Qdrant (Vector Database) - For storing 100k+ product embeddings.
*   **Infrastructure**: Docker, Redis (Task Queue), GPU Support (CUDA).

## 💡 Key Features
1.  **"Vibe Check" Endpoint**: Upload an image -> Get a structured JSON breakdown of the *vibe*, *occasion*, and *setting*.
2.  **"Magic Crop" Object Detection**: Automatically isolate fashion items from complex scenes.
3.  **Semantic Search**: Search for products using natural language ("outfit for a beach party") or image queries.

## 📅 Roadmap for "Green Squares"
1.  **Core API Setup**: FastAPI boilerplate and configuration.
2.  **Database Layer**: Qdrant connection and schema design.
3.  **Vision Service**: Owlv2 integration for detection.
4.  **Embedding Service**: SigLIP pipeline for vectors.
5.  **Search Logic**: The retrieval engine connecting it all.
