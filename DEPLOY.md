# Deployment Guide

## Production Checklist

? **Code**
- Backend refactored for performance & security
- Frontend optimized builds
- 4 worker processes configured
- Security headers added
- Rate limiting enabled

? **Configuration**
- Environment variables externalized
- Secrets not in version control
- Database pooling optimized
- Logging centralized (JSON format)
- Health checks configured

? **Infrastructure**
- Docker containers ready
- Healthchecks for all services
- Service dependencies defined
- Volumes for data persistence

## Quick Deployment

### Local/Dev
```bash
# Configure
cp .env.example .env
# Edit .env: add OPENAI_API_KEY, GOOGLE_API_KEY, GROQ_API_KEY

# Run
docker compose up --build

# Verify
curl http://localhost:8000/health
curl http://localhost:3000
```

### Production (AWS/GCP/Digital Ocean)
```bash
# 1. Build images
docker build -t maipaep-backend:latest backend/
docker build -t maipaep-frontend:latest frontend/

# 2. Push to registry
docker tag maipaep-backend:latest myregistry/maipaep-backend:latest
docker push myregistry/maipaep-backend:latest
docker tag maipaep-frontend:latest myregistry/maipaep-frontend:latest
docker push myregistry/maipaep-frontend:latest

# 3. Deploy via docker-compose (on server)
docker-compose -f docker-compose.yml up -d

# 4. Configure reverse proxy (Nginx/Traefik)
# See proxy config below
```

## Architecture Diagram

```
User ? Nginx (Reverse Proxy, SSL/TLS)
        +-- Frontend (3000 ? port 3000)
        +-- Backend (8000 ? port 8000)
             +-- API (FastAPI)
             +-- PostgreSQL (5432)
             +-- MongoDB (27017)
             +-- Redis (6379)
```

## Environment Variables (Production)

```env
# Required
OPENAI_API_KEY=sk-proj-...
GOOGLE_API_KEY=AIza...
GROQ_API_KEY=gsk_...

# Recommended - Strong values for production
SECRET_KEY=your-long-random-string-here-min-32-chars
JWT_SECRET=another-long-random-string-here-min-32-chars
ENCRYPTION_KEY=yet-another-long-random-string-min-32-chars

# Database URLs (update host if not localhost)
POSTGRES_URL=postgresql://maipaep_user:strong_password@postgres:5432/maipaep
MONGODB_URL=mongodb://maipaep_user:strong_password@mongodb:27017/maipaep
REDIS_URL=redis://:strong_password@redis:6379/0

# URLs
BACKEND_URL=https://api.yourdomain.com
FRONTEND_URL=https://yourdomain.com
NEXT_PUBLIC_API_URL=https://api.yourdomain.com/api/v1

# Security
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Environment
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
```

## Nginx Reverse Proxy Config

```nginx
upstream backend {
    server backend:8000;
}

upstream frontend {
    server frontend:3000;
}

server {
    listen 80;
    server_name _;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 60s;
    }
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    location / {
        proxy_pass http://frontend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Monitoring & Health

### Health Check
```bash
curl https://api.yourdomain.com/health
# Returns: { "status": "healthy", "services": {...} }
```

### Logs
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Performance Metrics
- API: `GET /metrics` (Prometheus format)
- Frontend: Browser DevTools, Lighthouse
- Database: Query performance logs in PostgreSQL

## Backup & Recovery

### PostgreSQL
```bash
# Backup
docker exec maipaep-postgres pg_dump -U maipaep_user maipaep > backup.sql

# Restore
docker exec -i maipaep-postgres psql -U maipaep_user maipaep < backup.sql
```

### MongoDB
```bash
# Backup
docker exec maipaep-mongodb mongodump -u maipaep_user -p maipaep_password --out /backup

# Restore
docker exec maipaep-mongodb mongorestore --drop -u maipaep_user -p maipaep_password /backup
```

## Scaling

### Horizontal
- Add multiple backend containers + load balancer
- Use managed databases (RDS, MongoDB Atlas)
- Use managed Redis (ElastiCache, Redis Cloud)

### Vertical
- Increase workers: Set `WORKERS=8` in .env
- Increase DB connection pool: `DB_POOL_SIZE=50`
- Enable caching: `CACHE_ENABLED=true`

## Security Best Practices

? Use HTTPS/TLS (Let's Encrypt)
? Rotate secrets regularly
? Use secret manager (AWS Secrets, Vault)
? Enable WAF on load balancer
? Rate limiting (built-in via FastAPI)
? CORS configured to domain only
? Security headers sent (X-Frame-Options, CSP, etc.)
? Input validation on all endpoints
? SQL injection prevention (SQLAlchemy ORM)
? CSRF protection ready

## Troubleshooting

### 502 Bad Gateway
- Check backend logs: `docker-compose logs backend`
- Verify API keys in .env
- Check database connectivity

### Frontend blank page
- Check browser console for API errors
- Verify NEXT_PUBLIC_API_URL points to correct backend
- Rebuild frontend: `docker-compose up --build frontend`

### Database connection errors
- Check credentials in .env
- Verify database volume persisted
- Check database healthcheck: `docker-compose ps`

---

**Ready to deploy!** Follow the steps above for your cloud provider.
