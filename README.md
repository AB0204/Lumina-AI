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

## 📅 Development Progress
- ✅ **Day 1**: Backend core (FastAPI, Owlv2, SigLIP, Qdrant)
- ✅ **Day 2**: Frontend setup (Next.js 15, TypeScript, Tailwind)
- ✅ **Day 3**: Image upload + Object detection UI
- ✅ **Day 4**: Bounding box visualization on canvas
- ✅ **Day 5**: Semantic search integration with SigLIP
- ✅ **Day 6**: UI polish, demo examples, and documentation
- 🚧 **Day 7**: Deployment preparation (coming next)
