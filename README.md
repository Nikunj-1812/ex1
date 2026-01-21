# MAI-PAEP - Production Ready

Multi-AI prompt evaluation platform. Compare responses from OpenAI, Google, and Groq in real-time with ML-powered scoring.

**Status:** ? Production Ready | **Version:** 1.0.0

## Quick Deploy

```bash
# Set up environment
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY, GOOGLE_API_KEY, GROQ_API_KEY

# Build and run
docker-compose up --build

# Verify
curl http://localhost:8000/health
open http://localhost:3000
```

## Architecture

- **Backend:** FastAPI (Python 3.11) + PostgreSQL + MongoDB + Redis
- **Frontend:** Next.js 14 + React 18 + Tailwind CSS
- **ML:** Sentence-transformers, spaCy, PyTorch
- **Infra:** Docker Compose (3+ containers)

## Features

- Multi-model querying (OpenAI GPT-4, Google Gemini, Groq LLaMA/Mistral)
- Real-time response evaluation (relevance, accuracy, clarity, hallucination risk, bias, trust)
- ML-powered domain classification + safety warnings
- Interactive dashboards with charts
- Cost + latency tracking per model
- RESTful API + Swagger docs

## Production URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| Health | http://localhost:8000/health |

For your domain:
- Frontend: `https://yourdomain.com`
- API: `https://api.yourdomain.com`

## Security

? CSRF protection  
? XSS headers  
? CORS configured  
? Rate limiting (config in .env)  
? Input validation  
? Secure password hashing  
? JWT tokens ready  

## Performance

- 4 Uvicorn workers (configurable)
- GZip compression enabled
- Request caching via Redis
- Async/await throughout
- DB connection pooling
- Frontend optimized builds

## API Example

```bash
curl -X POST http://localhost:8000/api/v1/prompt/submit \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain quantum computing",
    "selected_models": ["gpt-4-turbo-preview", "gemini-pro", "llama-3-70b"]
  }'
```

Response includes domain classification, per-model scores, comparison ranking, cost, latency.

## Environment Variables

**Required:**
- `OPENAI_API_KEY` — OpenAI key
- `GOOGLE_API_KEY` — Google AI Studio key
- `GROQ_API_KEY` — Groq key

**Optional but recommended:**
- `MISTRAL_API_KEY` — Mistral LLM (via Groq fallback)
- `SECRET_KEY` — JWT signing (auto-generated if missing)
- `JWT_SECRET` — Token encryption (auto-generated if missing)

See `.env.example` for all options.

## Documentation

- [QUICKSTART.md](QUICKSTART.md) — Get running in 5 minutes
- [LAUNCH_GUIDE.md](LAUNCH_GUIDE.md) — Deploy to prod
- [docs/API.md](docs/API.md) — API reference

## Deployment

### Docker (Recommended)
```bash
docker-compose -f docker-compose.yml up -d
docker-compose ps
docker-compose logs -f backend
```

### Kubernetes / Cloud
1. Build images: `docker build -t maipaep-backend backend/`
2. Push to registry: `docker push yourreg/maipaep-backend:latest`
3. Deploy manifests (K8s YAML or Terraform)
4. Set env vars from secrets manager

### Monitoring
- Health check: `GET /health`
- Metrics: `GET /metrics` (Prometheus-ready)
- Logs: JSON format, aggregated to stdout

## Support

For issues, bugs, or feature requests, check:
1. API error response (includes detail)
2. Container logs: `docker-compose logs`
3. DB connectivity: `docker exec maipaep-postgres psql -U maipaep_user -d maipaep`

---

**License:** MIT | **Author:** MAI-PAEP | **Updated:** Jan 2026
