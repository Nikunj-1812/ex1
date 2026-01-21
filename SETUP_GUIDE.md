# MAI-PAEP Setup Guide

**Multi-AI Prompt Intelligence & Accuracy Evaluation Platform**

## Quick Start (5 Minutes)

### Prerequisites
- Docker and Docker Compose installed
- API keys from OpenAI, Google, and Groq

### Step 1: Add API Keys
Edit the `.env` file and add your API keys:
```env
OPENAI_API_KEY=sk-your-actual-key-here
GOOGLE_API_KEY=AIzaSy-your-actual-key-here
GROQ_API_KEY=gsk_your-actual-key-here
```

### Step 2: Start Application
```bash
docker-compose up --build
```

### Step 3: Access Application
- Frontend: http://localhost:3000
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

That's it! The application is now running.

---

## Getting API Keys

### OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)

### Google AI API Key
1. Go to https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key (starts with `AIzaSy`)

### Groq API Key
1. Go to https://console.groq.com/keys
2. Sign up or log in
3. Click "Create API Key"
4. Copy the key (starts with `gsk_`)

---

## Architecture

### Services Running
- **Frontend** (port 3000): Next.js 14 with React 18
- **Backend** (port 8000): FastAPI with 4 workers
- **PostgreSQL** (port 5432): Analytics and logs
- **MongoDB** (port 27017): AI responses storage
- **Redis** (port 6379): Caching layer

### Technology Stack
- **Frontend**: Next.js 14, React 18, TypeScript, Tailwind CSS, Framer Motion
- **Backend**: FastAPI, Python 3.11, Pydantic v2
- **AI Models**: GPT-4, Claude 3, Gemini Pro, LLaMA 3, Mistral
- **ML/NLP**: Sentence-BERT, Transformers, spaCy
- **Databases**: PostgreSQL 15, MongoDB 7, Redis 7

---

## Features

### AI Model Comparison
- Compare responses from 7 different AI models simultaneously
- Side-by-side evaluation with detailed scoring

### ML-Powered Evaluation
- **Accuracy Score**: Semantic correctness and factual accuracy
- **Relevance Score**: How well response matches prompt intent
- **Clarity Score**: Readability and structure analysis
- **Hallucination Detection**: Identifies unsourced claims
- **Trust Score**: Composite reliability metric

### Advanced Analytics
- Domain classification (medical, legal, coding, etc.)
- Safety level assessment with warnings
- Performance metrics (speed, cost, token usage)
- Visual comparison charts

### User Experience
- Real-time progress tracking
- Interactive dashboards
- Export results as JSON
- Dark mode support
- Responsive design

---

## Usage

### Basic Workflow
1. Enter your prompt in the text area
2. Select 2 or more AI models to compare
3. Click "Compare AI Models"
4. Wait for analysis (typically 5-15 seconds)
5. Review detailed comparisons and scores
6. Export results if needed

### Tips for Best Results
- Be specific and clear in your prompts
- Select at least 2 models for meaningful comparison
- Review the domain classification for context
- Pay attention to hallucination warnings
- Use trust scores to identify most reliable responses

---

## Configuration

### Environment Variables
All configuration is in `.env` file:
- **AI API Keys**: Required for model access
- **Database URLs**: Auto-configured for Docker
- **Security Keys**: Generate random values for production
- **Feature Flags**: Enable/disable specific features

### Customization
- **Model Selection**: Edit `frontend/src/app/page.tsx` to change available models
- **Scoring Weights**: Adjust in `ml/evaluator/` files
- **UI Theme**: Modify `frontend/src/app/globals.css`

---

## Troubleshooting

### Application won't start
```bash
# Check Docker is running
docker --version

# View service logs
docker-compose logs backend
docker-compose logs frontend

# Restart services
docker-compose down
docker-compose up --build
```

### API returns errors
- Verify API keys are correct in `.env`
- Check API key has sufficient credits/quota
- Review backend logs: `docker-compose logs backend`

### Database connection failed
```bash
# Restart database services
docker-compose restart postgres mongodb redis

# Check database logs
docker-compose logs postgres
```

### Frontend not loading
```bash
# Check frontend logs
docker-compose logs frontend

# Verify NEXT_PUBLIC_API_URL in .env
# Should be: http://localhost:8000/api/v1

# Rebuild frontend
docker-compose up --build frontend
```

---

## Development

### Backend Development
```bash
# Access backend container
docker-compose exec backend bash

# Run tests
docker-compose exec backend pytest

# Check code style
docker-compose exec backend black app/
```

### Frontend Development
```bash
# Access frontend container
docker-compose exec frontend sh

# Install new package
docker-compose exec frontend npm install package-name

# Run linter
docker-compose exec frontend npm run lint
```

### Database Access
```bash
# PostgreSQL
docker-compose exec postgres psql -U maipaep_user -d maipaep

# MongoDB
docker-compose exec mongodb mongosh -u maipaep_user -p maipaep_password maipaep

# Redis
docker-compose exec redis redis-cli
```

---

## Production Deployment

### Security Checklist
- [ ] Generate strong random SECRET_KEY, JWT_SECRET, ENCRYPTION_KEY
- [ ] Use environment-specific API keys
- [ ] Enable HTTPS/TLS
- [ ] Configure firewall rules
- [ ] Set up monitoring and alerting
- [ ] Regular database backups
- [ ] Rotate API keys periodically

### Deployment Options
- **Docker Compose**: Simplest, single-server deployment
- **Kubernetes**: Scalable, multi-server deployment
- **Cloud Platforms**: AWS ECS, Google Cloud Run, Azure Container Instances

---

## Support

### Documentation
- API Documentation: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

### Common Commands
```bash
# View all logs
docker-compose logs -f

# Stop everything
docker-compose down

# Restart specific service
docker-compose restart backend

# Check service health
curl http://localhost:8000/health

# Export database
docker-compose exec postgres pg_dump -U maipaep_user maipaep > backup.sql
```

---

## Performance

### Expected Response Times
- Domain Classification: <100ms
- AI Model Query: 2-10 seconds per model
- ML Evaluation: <500ms per response
- Total Processing: 5-15 seconds (depending on models selected)

### Cost Estimation
Typical costs per prompt comparison (3 models):
- GPT-4: ~$0.01-0.03
- GPT-3.5: ~$0.001-0.002
- Claude 3: ~$0.01-0.02
- Gemini Pro: ~$0.001-0.003
- LLaMA/Mistral (via Groq): ~$0.001-0.002

**Total**: ~$0.02-0.06 per comparison

---

## License

This project is provided as-is for evaluation and deployment.

---

## What's Next?

1. **Start Application**: `docker-compose up --build`
2. **Add API Keys**: Edit `.env` file
3. **Test Prompt**: Visit http://localhost:3000
4. **Review Documentation**: Check http://localhost:8000/docs
5. **Explore Features**: Try different prompts and model combinations

For questions or issues, check the logs with `docker-compose logs` or review the troubleshooting section above.
