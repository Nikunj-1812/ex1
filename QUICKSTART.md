# Quick Start

## 1) Configure
- Copy .env.example to .env if needed
- Add API keys: OPENAI_API_KEY, GOOGLE_API_KEY, GROQ_API_KEY

## 2) Run with Docker (recommended)
```
docker-compose up --build
```
- Frontend: http://localhost:3000
- API docs: http://localhost:8000/docs

## 3) Manual Dev (if not using Docker)
Backend:
```
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
Frontend:
```
cd frontend
npm install
npm run dev
```

## 4) Smoke Test
- GET http://localhost:8000/health
- POST http://localhost:8000/api/v1/prompt/submit with prompt + selected_models
- Open the UI at http://localhost:3000 and send a prompt

## 5) Troubleshooting
- Missing keys ? recheck .env
- Ports busy ? change 3000/8000 or stop conflicting processes
- Models slow ? reduce selected_models count during testing
