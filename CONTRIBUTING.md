# Contributing to Lumina AI

Thank you for your interest in contributing! Here's how to get started.

## 🚀 Quick Setup

1. **Fork & Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Lumina-AI.git
   cd Lumina-AI
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   uvicorn app.main:app --reload
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Docker (Full Stack)**
   ```bash
   docker-compose up --build
   ```

## 📝 Guidelines

- Follow existing code style
- Write descriptive commit messages
- Add tests for new features
- Update documentation as needed

## 🐛 Bug Reports

Open an issue with:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots (if applicable)

## 📬 Pull Requests

1. Create a feature branch: `git checkout -b feat/your-feature`
2. Make changes and commit
3. Push and open a PR against `main`
