# Contributing to Lumina AI

First off, thanks for taking the time to contribute! 🎉

The following is a set of guidelines for contributing to Lumina AI. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## 🛠️ Development Setup

1. **Fork the repository** on GitHub.
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Lumina-AI.git
   cd Lumina-AI
   ```
3. **Install dependencies**:
   ```bash
   # Backend
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt

   # Frontend
   cd ../frontend
   npm install
   ```
4. **Environment Variables**:
   Copy `.env.example` to `.env` (if available) or create `.env.local` in `frontend/` with:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

5. **Running the App**:
   - Backend: `uvicorn main:app --reload` (port 8000)
   - Frontend: `npm run dev` (port 3000)

## 🐛 Reporting Bugs

Bugs are tracked as GitHub issues. When creating an issue, please include:
- A clear and descriptive title
- Steps to reproduce the problem
- Expected behavior vs actual behavior
- Screenshots (if applicable)

## 💡 Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:
- A clear and descriptive title
- Detailed description of the proposed enhancement
- Why this enhancement would be useful

##  pull Requests

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. Ensure the test suite passes.
4. Make sure your code lints.
5. descriptive commit messages are appreciated!

## 📜 License

By contributing, you agree that your contributions will be licensed under its MIT License.
