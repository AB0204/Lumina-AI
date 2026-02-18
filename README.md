# Lumina - The AI-Powered Style Engine

![Build Status](https://github.com/AB0204/Lumina-AI/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.11-blue)
![Next.js](https://img.shields.io/badge/next.js-15-black)
[![Demo](https://img.shields.io/badge/🎬_Live_Demo-Hugging_Face-yellow)](https://huggingface.co/spaces/Ab0202000/lumina-ai-demo)

> 🎬 **[Try Live Demo](https://huggingface.co/spaces/Ab0202000/lumina-ai-demo)** — Runs FREE on Hugging Face Spaces!

**[📊 Benchmarks](./BENCHMARKS.md)** • **[🏗️ Architecture](./ARCHITECTURE.md)** • **[🎮 Demo](https://huggingface.co/spaces/Ab0202000/lumina-ai-demo)** • **[🐳 Docker](#-deployment-docker)**

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

## ⚡ Performance Highlights

| Metric | Value |
|--------|-------|
| Cache Hit Latency | <10ms |
| Vector Search | <5ms |
| Total (w/ Cache) | <2ms |
| Model Memory | ~3.2GB |

> See [BENCHMARKS.md](./BENCHMARKS.md) for detailed performance analysis

## 🏗️ System Architecture

View the complete [Architecture Diagram](./ARCHITECTURE.md) showing the request flow through Redis caching, ML pipeline (OWLv2, SigLIP), and Qdrant vector search.

## 🏗️ Project Structure
```
Lumina/
├── backend/           # FastAPI backend
│   ├── app/
│   │   ├── api/      # API endpoints
│   │   ├── core/     # Configuration
│   │   └── services/ # AI model services
│   └── requirements.txt
├── frontend/          # Next.js 15 frontend
│   ├── app/          # App router pages
│   ├── components/   # React components
│   ├── lib/          # API client & utilities
│   └── types/        # TypeScript types
└── docker-compose.yml
```

## 🚀 Quick Start

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:3000` for the UI and `http://localhost:8000/docs` for API docs.

## 🎬 Live Demo

Want to try Lumina without installing anything? Deploy a fully functional demo to **Hugging Face Spaces for FREE**!

### What's Included in the Demo
- ✅ **Object Detection**: Upload fashion images and see AI-powered bounding boxes
- ✅ **Vibe Check**: Get style analysis (occasion, aesthetic, mood)
- ✅ **Semantic Search**: Natural language product search

### Deploy in 5 Minutes
See the [demo/README.md](./demo/) for step-by-step deployment instructions.

**Free Tier**: CPU-only (15-20s inference) - $0 forever ✅  
**Paid Tier**: GPU acceleration (2-3s inference) - ~$0.60/hour (optional)


## 🐳 Deployment (Docker)

Run the entire stack with a single command:

```bash
# Build and start all services
docker-compose up --build -d
```

Services will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/docs
- **Qdrant UI**: http://localhost:6333/dashboard
- **Redis**: http://localhost:6379
