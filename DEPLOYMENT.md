# 🚀 Production Deployment Guide

**Project Status**: ✅ **PRODUCTION-READY**  
**Last Updated**: 2024  
**Environment**: Docker Compose (Local/Remote)

---

## 📋 Pre-Deployment Checklist

- [x] All secrets removed from codebase (`.env` is template-only)
- [x] API keys configured in `.env` file (user-provided)
- [x] Docker images optimized for production
- [x] Security hardening applied (CORS, CSP, HSTS headers)
- [x] Database migrations prepared (init.sql)
- [x] All required Python/Node dependencies listed in `requirements.txt` and `package.json`
- [x] Health check endpoints configured
- [x] Logging configured (JSON format, INFO level)
- [x] Code is syntax-validated and error-free

---

## 🔧 Quick Setup (5 minutes)

### Step 1: Configure Environment
```bash
# Copy template to .env and add your API keys
cp .env.example .env

# Edit .env with your API keys:
# - OPENAI_API_KEY
# - GOOGLE_API_KEY
# - GROQ_API_KEY
```

### Step 2: Start Services
```bash
docker-compose up --build
```

### Step 3: Verify Deployment
```bash
# Check services are healthy
curl http://localhost:8000/health
curl http://localhost:3000

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

---

## 🐳 Docker Compose Architecture

| Service | Port | Technology | Health Check |
|---------|------|-----------|--------------|
| **Backend** | 8000 | FastAPI (4 workers) | `/health` (30s) |
| **Frontend** | 3000 | Next.js 14 | `GET /` (30s) |
| **PostgreSQL** | 5432 | Database (primary) | TCP check (10s) |
| **MongoDB** | 27017 | NoSQL store | TCP check (10s) |
| **Redis** | 6379 | Cache layer | TCP check (10s) |

### Service Dependencies
```
Frontend (port 3000)
    ↓
Backend (port 8000)
    ├→ PostgreSQL (port 5432)
    ├→ MongoDB (port 27017)
    └→ Redis (port 6379)
```

---

## 📍 Production URLs

### Development / Local
- Frontend: http://localhost:3000
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs (Swagger)
- API ReDoc: http://localhost:8000/redoc

### Production (Example)
- Frontend: https://app.example.com
- API: https://api.example.com
- Metrics: https://api.example.com/metrics

---

## 🔐 Security Checklist

**Backend Security:**
- ✅ CORS configured (whitelist specified origins)
- ✅ Security headers: X-Content-Type-Options, X-Frame-Options, X-XSS-Protection, HSTS, CSP
- ✅ Request validation via Pydantic v2
- ✅ Password hashing with bcrypt
- ✅ JWT-ready authentication layer
- ✅ Rate limiting (via middleware, configurable)
- ✅ SQL injection prevention (SQLAlchemy ORM + parameterized queries)

**Frontend Security:**
- ✅ No source maps in production (`productionBrowserSourceMaps: false`)
- ✅ Security headers added to all responses
- ✅ SWC minification enabled
- ✅ X-Powered-By header removed
- ✅ Referrer policy: strict-origin-when-cross-origin

**Infrastructure Security:**
- ✅ All API keys stored in `.env` (NOT in code)
- ✅ `.env` in `.gitignore` (never committed)
- ✅ `.env.example` provided as template
- ✅ Database credentials in environment variables
- ✅ Redis password enabled (optional, recommended)

---

## 📊 Performance Optimizations

**Backend:**
- ✅ 4-worker Uvicorn configuration (production mode)
- ✅ Async/await throughout for high concurrency
- ✅ GZip compression on responses (gzip_min_size=1000)
- ✅ Request-response timing middleware
- ✅ Database connection pooling
- ✅ Redis caching layer

**Frontend:**
- ✅ SWC minification (faster than Babel)
- ✅ GZip compression enabled
- ✅ No browser source maps
- ✅ Image optimization
- ✅ Code splitting (automatic via Next.js)
- ✅ Static export capability (if needed)

**Database:**
- ✅ PostgreSQL indexes on frequently queried columns
- ✅ MongoDB TTL indexes for temporary data
- ✅ Redis for session/cache storage

---

## 🚀 Deployment Methods

### Method 1: Docker Compose (Recommended for testing)
```bash
# Build and start
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Method 2: Kubernetes (Production Scaling)
```bash
# Prerequisites: kubectl, helm configured
# Build images and push to registry:
docker build -t yourreg/backend:latest ./backend
docker build -t yourreg/frontend:latest ./frontend

# Deploy via Helm or kubectl manifests:
kubectl create namespace aitoai
kubectl apply -f k8s/ -n aitoai
```

### Method 3: Cloud Platforms

**AWS (ECS/Fargate):**
```bash
# Push to ECR, create task definitions, deploy
aws ecr create-repository --repository-name backend
aws ecr create-repository --repository-name frontend
# ... configure ECS cluster
```

**Google Cloud (Cloud Run):**
```bash
# Deploy containerized backend/frontend
gcloud run deploy backend --image yourreg/backend:latest
gcloud run deploy frontend --image yourreg/frontend:latest
```

**Azure (Container Instances):**
```bash
# Upload images to ACR
az acr build --registry <registry-name> --image backend:latest ./backend
az acr build --registry <registry-name> --image frontend:latest ./frontend
```

---

## 📈 Monitoring & Health

### Health Check Endpoints
```bash
# Backend Health
curl http://localhost:8000/health

# Response:
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "services": {
    "api": "operational",
    "database": "connected",
    "cache": "connected"
  }
}
```

### Metrics Endpoint
```bash
# Get Prometheus metrics
curl http://localhost:8000/metrics
```

### View Logs
```bash
# Docker Compose
docker-compose logs -f --tail=100

# Specific service
docker-compose logs backend -f

# With timestamps
docker-compose logs -f -t
```

---

## 🧪 Testing API

### List All AI Models
```bash
curl -X GET http://localhost:8000/api/v1/models
```

### Submit Prompt to Multiple Models
```bash
curl -X POST http://localhost:8000/api/v1/prompt/submit \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain quantum computing in simple terms",
    "selected_models": ["gpt-4-turbo-preview", "gemini-pro", "llama-3-70b"],
    "context": "educational"
  }'
```

### Get Comparison Results
```bash
curl -X GET http://localhost:8000/api/v1/results/compare \
  -H "Content-Type: application/json" \
  -d '{
    "metric": "clarity_score",
    "order": "desc"
  }'
```

---

## 🔧 Troubleshooting

### Frontend won't start
```bash
# Check if port 3000 is in use
# Solution: Change port in docker-compose.yml or kill process on port 3000

# Check logs
docker-compose logs frontend
```

### Backend fails to connect to database
```bash
# Verify PostgreSQL is running
docker-compose logs postgres

# Check POSTGRES_URL in .env
# Format: postgresql+asyncpg://user:password@host:port/dbname
```

### API returning 500 errors
```bash
# Check backend logs for detailed error
docker-compose logs -f backend

# Verify all required env vars are set
# Verify database migrations ran: SELECT * FROM alembic_version;
```

### High latency or memory usage
```bash
# Check container resource usage
docker stats

# Increase container memory limits in docker-compose.yml
# Increase database connection pool size if needed
```

---

## 📦 Environment Variables Reference

```env
# AI API Keys (Required - user provides)
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=AIzaSy...
GROQ_API_KEY=gsk_...
MISTRAL_API_KEY=... (optional)

# Database URLs
POSTGRES_URL=postgresql+asyncpg://postgres:password@postgres:5432/aitoai_db
MONGODB_URL=mongodb://mongodb:27017/aitoai_db
REDIS_URL=redis://:password@redis:6379/0

# Application
APP_NAME=AI-to-AI
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
LOG_FORMAT=json

# Security
SECRET_KEY=your-secret-key-here (32+ chars)
JWT_SECRET=your-jwt-secret-here (32+ chars)
ENCRYPTION_KEY=your-encryption-key-here (32+ chars)

# URLs
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000

# AI Models (Defaults)
DEFAULT_GPT_MODEL=gpt-4-turbo-preview
DEFAULT_GOOGLE_MODEL=gemini-pro
DEFAULT_GROQ_MODEL=llama-3-70b-versatile
DEFAULT_MISTRAL_MODEL=mistral-large-latest

# ML Configuration
ML_DEVICE=cpu (or cuda for GPU)
ML_BATCH_SIZE=32
ML_MAX_LENGTH=512

# Workers
UVICORN_WORKERS=4

# CORS
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]
```

---

## 🔄 Continuous Deployment (CI/CD)

### GitHub Actions Example
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build and push Docker images
        run: |
          docker build -t ${{ secrets.DOCKER_REGISTRY }}/backend:latest ./backend
          docker build -t ${{ secrets.DOCKER_REGISTRY }}/frontend:latest ./frontend
          docker push ${{ secrets.DOCKER_REGISTRY }}/backend:latest
          docker push ${{ secrets.DOCKER_REGISTRY }}/frontend:latest
      - name: Deploy to production
        run: ./deploy.sh
```

---

## ✅ Verification Checklist

After deployment, verify:

- [ ] Frontend loads without errors
- [ ] API responds to requests (check `/health`)
- [ ] Database is accessible
- [ ] Redis is accessible
- [ ] AI models return responses
- [ ] Logs are being generated
- [ ] Security headers are present (check with browser DevTools)
- [ ] Performance is acceptable (check metrics)
- [ ] Backups are configured (production databases)

---

## 📞 Support & Resources

- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **GitHub**: [Your repository URL]
- **Issues**: Check logs with `docker-compose logs`

---

**Status**: ✅ Ready for Production  
**Next Step**: Follow "Quick Setup (5 minutes)" section above
