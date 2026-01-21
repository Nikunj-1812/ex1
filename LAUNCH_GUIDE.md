# Launch Guide

## Preflight
- .env has API keys (OpenAI, Google, Groq)
- Docker installed (or Python 3.11 + Node 18 for manual)

## Option A: Docker Compose
```
docker-compose up --build
```
Services: backend 8000, frontend 3000, postgres 5432, mongodb 27017, redis 6379

## Option B: Manual (dev)
1) Datastores (if not using Docker): run Postgres, MongoDB, Redis locally
2) Backend
```
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
3) Frontend
```
cd frontend
npm install
npm run dev
```

## Verification
- API health: GET http://localhost:8000/health
- API docs: http://localhost:8000/docs
- Submit prompt: POST http://localhost:8000/api/v1/prompt/submit with { prompt, selected_models }
- UI: http://localhost:3000 ? enter a prompt, select models, check results

## Production Notes
- Keep real secrets outside version control; load via env vars/secret manager
- Set strong SECRET_KEY and JWT_SECRET
- Enable HTTPS/SSL at your edge (reverse proxy or cloud LB)
- Persist Postgres/Mongo volumes; secure Redis with a password
- Scale services behind a process manager or container orchestrator if needed
