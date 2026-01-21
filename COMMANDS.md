# 🔧 Command Reference Guide

Quick access to all essential commands for development and deployment.

---

## 🚀 Getting Started (Must Run First)

```bash
# 1. Setup environment
cp .env.example .env

# 2. Start all services
docker-compose up --build

# 3. Test services
curl http://localhost:8000/health
open http://localhost:3000
```

---

## 📦 Docker Commands

### Start/Stop
```bash
# Start in foreground (see logs)
docker-compose up

# Start in background
docker-compose up -d --build

# Stop all services
docker-compose down

# Stop and remove volumes (CAREFUL: deletes data)
docker-compose down -v

# Restart specific service
docker-compose restart backend
docker-compose restart frontend

# Rebuild and start
docker-compose up -d --build
```

### View Status
```bash
# See all running containers
docker-compose ps

# See all services (including stopped)
docker-compose ps --all

# View resource usage
docker stats

# Check container logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs -f           # Follow logs
docker-compose logs --tail=100   # Last 100 lines
docker-compose logs -t           # With timestamps

# View only errors
docker-compose logs | grep ERROR
```

### Execute Commands
```bash
# Open shell in container
docker-compose exec backend bash
docker-compose exec frontend bash

# Run one-off command
docker-compose exec backend python -c "print('hello')"

# Run command in new container (doesn't connect to running app)
docker-compose run backend python -c "import fastapi; print(fastapi.__version__)"
```

### Cleanup
```bash
# Remove unused containers
docker container prune

# Remove unused images
docker image prune

# Remove unused networks
docker network prune

# Remove all unused resources
docker system prune -a

# View disk usage
docker system df
```

---

## 🐍 Python/Backend Commands

### Inside Container
```bash
# Access Python shell
docker-compose exec backend python

# Install/upgrade package
docker-compose exec backend pip install package-name

# Show installed packages
docker-compose exec backend pip list

# Run Python file
docker-compose exec backend python script.py
```

### Database
```bash
# Access PostgreSQL shell
docker-compose exec postgres psql -U postgres -d aitoai_db

# List tables
\dt

# View schema
\d table_name

# Export database
docker-compose exec postgres pg_dump -U postgres aitoai_db > backup.sql

# Import database
docker-compose exec -T postgres psql -U postgres aitoai_db < backup.sql
```

---

## 🎨 Frontend/Node Commands

### Inside Container
```bash
# Install dependencies
docker-compose exec frontend npm install

# Install specific package
docker-compose exec frontend npm install package-name

# Run build
docker-compose exec frontend npm run build

# Run development server (if needed for troubleshooting)
docker-compose exec frontend npm run dev

# Run linter
docker-compose exec frontend npm run lint

# View package.json scripts
docker-compose exec frontend npm run
```

---

## 🔍 API Testing

### Get API Version
```bash
curl http://localhost:8000
```

### Health Check
```bash
curl http://localhost:8000/health
```

### Get Available Models
```bash
curl http://localhost:8000/api/v1/models
```

### Submit Prompt
```bash
curl -X POST http://localhost:8000/api/v1/prompt/submit \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is artificial intelligence?",
    "selected_models": ["gpt-4-turbo-preview", "gemini-pro", "llama-3-70b-versatile"],
    "context": "general"
  }'
```

### Get Results
```bash
# Latest results
curl http://localhost:8000/api/v1/results/latest

# Compare results
curl http://localhost:8000/api/v1/results/compare

# Filter by metric
curl "http://localhost:8000/api/v1/results/compare?metric=clarity_score&order=desc"
```

### Get Metrics
```bash
curl http://localhost:8000/metrics
```

---

## 📊 Monitoring

### View Real-Time Stats
```bash
docker stats
```

### View Container Details
```bash
docker-compose exec backend nvidia-smi  # GPU status (if GPU enabled)

docker-compose ps --format "table {{.Names}}\t{{.Status}}"
```

### Check Ports
```bash
# Check if port is in use (Windows PowerShell)
netstat -ano | findstr :8000
netstat -ano | findstr :3000

# Kill process on port (Windows PowerShell)
taskkill /PID <PID> /F
```

---

## 🔒 Security & Secrets

### View Environment Variables
```bash
# Show .env file
cat .env

# Show specific variable
grep OPENAI_API_KEY .env

# View in running container
docker-compose exec backend env | grep OPENAI
```

### Rotate API Keys
```bash
# 1. Update .env with new key
nano .env

# 2. Restart service
docker-compose restart backend
```

---

## 📈 Performance Tuning

### Increase Worker Processes
```bash
# Edit docker-compose.yml
# Change: --workers 4 → --workers 8
# Then restart
docker-compose restart backend
```

### Check Database Performance
```bash
# Inside PostgreSQL shell
docker-compose exec postgres psql -U postgres -d aitoai_db

# Show slow queries
SELECT query, mean_time FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;

# Analyze table
ANALYZE table_name;

# Index creation
CREATE INDEX idx_name ON table_name(column);
```

### Monitor Redis
```bash
# Connect to Redis
docker-compose exec redis redis-cli

# Show memory usage
INFO memory

# Show keys
KEYS *

# Show stats
INFO stats
```

---

## 🐛 Debugging

### Check Application Logs
```bash
# Backend errors
docker-compose logs backend | grep ERROR

# Frontend build errors
docker-compose logs frontend | grep -i error

# Database connection errors
docker-compose logs postgres | grep -i error
```

### Common Issues

**Port Already in Use**
```bash
# Find and kill process
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or change port in docker-compose.yml
```

**Out of Memory**
```bash
# Check disk space
df -h
docker system df

# Clean up
docker system prune -a
```

**Network Issues**
```bash
# Check network
docker network ls
docker network inspect maipaep-network

# Test connectivity
docker-compose exec backend ping mongodb
docker-compose exec backend ping redis
```

---

## 🚢 Deployment

### Build Images for Registry
```bash
# Build backend image
docker build -t myregistry/backend:latest ./backend

# Build frontend image
docker build -t myregistry/frontend:latest ./frontend

# Tag with version
docker tag myregistry/backend:latest myregistry/backend:v1.0.0

# Push to registry
docker push myregistry/backend:latest
docker push myregistry/frontend:latest
```

### Deploy to Docker Hub
```bash
# Login
docker login

# Tag
docker tag backend:latest username/backend:latest

# Push
docker push username/backend:latest
```

### Deploy to Production
```bash
# SSH to server
ssh user@server.com

# Pull latest code
cd /app
git pull origin main

# Update .env
nano .env

# Rebuild and restart
docker-compose up -d --build

# Verify
docker-compose ps
curl http://localhost:8000/health
```

---

## 📚 Useful Aliases (Add to .bashrc or .zshrc)

```bash
# Docker Compose shortcuts
alias dc='docker-compose'
alias dcup='docker-compose up -d --build'
alias dcdown='docker-compose down'
alias dclogs='docker-compose logs -f'
alias dcps='docker-compose ps'

# Backend access
alias backend-shell='docker-compose exec backend bash'
alias backend-python='docker-compose exec backend python'
alias backend-pip='docker-compose exec backend pip'

# Frontend access
alias frontend-shell='docker-compose exec frontend bash'
alias frontend-npm='docker-compose exec frontend npm'

# Database access
alias db-shell='docker-compose exec postgres psql -U postgres -d aitoai_db'
alias redis-shell='docker-compose exec redis redis-cli'

# Logs
alias logs-backend='docker-compose logs -f backend'
alias logs-frontend='docker-compose logs -f frontend'
alias logs-db='docker-compose logs -f postgres'

# Cleanup
alias docker-clean='docker system prune -a'
```

---

## 🎯 Quick Troubleshooting

| Issue | Command |
|-------|---------|
| Services won't start | `docker-compose logs` |
| API not responding | `curl http://localhost:8000/health` |
| Database error | `docker-compose logs postgres` |
| Frontend blank | `docker-compose logs frontend` |
| High memory | `docker system prune -a` |
| Port in use | `netstat -ano \| findstr :PORT` |
| Can't connect to DB | `docker-compose exec backend ping postgres` |
| Need shell access | `docker-compose exec backend bash` |

---

## 📖 More Information

- Docker Compose Docs: https://docs.docker.com/compose/
- FastAPI Docs: https://fastapi.tiangolo.com/
- Next.js Docs: https://nextjs.org/docs/
- PostgreSQL Docs: https://www.postgresql.org/docs/
- MongoDB Docs: https://docs.mongodb.com/

---

**Last Updated**: 2024  
**Status**: Complete
