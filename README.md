# SnapShop - Intelligent Visual Commerce Engine

SnapShop is a backend API service that transforms "messy" real-world photos (e.g., street style, party photos) into purchasable product matches using advanced computer vision models.

## 🚀 The Concept
Input: Any unstructured image (JPEG/PNG)
Output: Distinct clothing items detected, cropped, and matched to similar purchasable products.

## 🛠️ The Tech Stack
*   **Core AI**:
    *   **Owlv2**: Zero-Shot Object Detection (detects "shirt", "dress", "shoes" without specific training).
    *   **SigLIP**: Embedding model for generating high-dimensional vector representations of cropped items.
*   **Backend**: FastAPI (Python) - High-performance async API for serving ML models.
*   **Database**: Qdrant (Vector Database) - Stores and searches product embeddings.
*   **Infrastructure**: Docker & Docker Compose.

## 💡 Key Features
1.  **"Magic Crop" Endpoint**:
    *   Send image -> Run Owlv2 -> Return bounding boxes for apparel items.
2.  **Visual Similarity Search**:
    *   Crop detected item -> Generate SigLIP embedding -> Query Qdrant for nearest neighbors.
3.  **Hybrid Filtering**:
    *   Filter visual search results with text queries (e.g., "blue denim jacket").

## 📅 Implementation Plan

### Week 1: Backend & AI Foundation
- [ ] Set up FastAPI project structure.
- [ ] Implement Owlv2 inference pipeline (Object Detection).
- [ ] Create API endpoint for image upload and detection.

### Week 2: Database & Search
- [ ] Deploy Qdrant with Docker.
- [ ] Implement SigLIP embedding pipeline.
- [ ] Build "Indexer" script to ingest product catalog.
- [ ] Connect Detection -> Embedding -> Search workflow.

## 📈 Why This Matters
*   Demonstrates ability to host and run open-source models (not just API calls).
*   Showcases Data Engineering skills with vector search at scale.
*   Builds a "holy grail" feature for modern e-commerce (Visual Search).

## 🏃 Getting Started

### Prerequisites
*   Python 3.10+
*   Docker & Docker Compose

### Running the API
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```
