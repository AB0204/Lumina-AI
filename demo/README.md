# Lumina AI - Gradio Demo

A fully functional demo showcasing Lumina's AI-powered visual commerce capabilities.

## 🚀 Deploy to Hugging Face Spaces (FREE)

### Quick Deploy
1. **Create a Space**:
   - Go to [Hugging Face Spaces](https://huggingface.co/spaces)
   - Click "Create new Space"
   - Name: `lumina-ai-demo`
   - SDK: Gradio
   - Hardware: **CPU basic (FREE)** ✅

2. **Upload Files**:
   ```bash
   # Clone your space
   git clone https://huggingface.co/spaces/YOUR_USERNAME/lumina-ai-demo
   cd lumina-ai-demo
   
   # Copy demo files
   cp /path/to/Lumina/demo/app.py .
   cp /path/to/Lumina/demo/requirements.txt .
   
   # Push to HF
   git add .
   git commit -m "Initial commit"
   git push
   ```

3. **Done!** Your demo will be live at `https://huggingface.co/spaces/YOUR_USERNAME/lumina-ai-demo`

### Performance Expectations

| Hardware | Cold Start | Inference | Cost |
|----------|-----------|-----------|------|
| **CPU (FREE)** | ~60s | 15-20s | $0 ✅ |
| T4 GPU | ~30s | 2-3s | ~$0.60/hr |
| A10G GPU | ~20s | <1s | ~$3.15/hr |

**Recommendation**: Use FREE CPU tier for portfolio/demo purposes.

## 🎯 Features

1. **Object Detection**: Upload fashion images → Get bounding boxes around detected items
2. **Vibe Check**: Analyze style, occasion, and aesthetic
3. **Semantic Search**: Text-to-image product search

## 🧪 Local Testing

```bash
cd demo
pip install -r requirements.txt
python app.py
```

Visit `http://localhost:7860` to test locally before deploying.

## 📝 Notes

- First load downloads models (~1GB) - takes ~60s on free tier
- Subsequent loads are faster (~5-10s)
- Models are cached automatically
- No authentication required for public demos
