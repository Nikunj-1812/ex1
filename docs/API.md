# API Reference

Base URL (dev): http://localhost:8000
Docs: /docs
Health: /health

## Authentication
No auth in dev. Add JWT before production.

## Endpoints

### GET `/`
Returns service info.

### GET `/health`
Returns overall health and dependency status.

### POST `/api/v1/prompt/submit`
Submit a prompt for multi-model evaluation.

**Request body**
```
{
  "prompt": "Explain quantum entanglement simply.",
  "selected_models": ["gpt-4-turbo-preview", "claude-3-opus-20240229"],
  "user_id": "optional"
}
```

**Key fields**
- prompt: string (10-4000 chars)
- selected_models: array of model ids

**Model ids**
- gpt-4-turbo-preview
- gpt-3.5-turbo
- claude-3-opus-20240229
- claude-3-sonnet-20240229
- gemini-pro
- llama-3-70b
- mistral-large-latest

**Success response (trimmed)**
```
{
  "session_id": "sess_xxx",
  "domain_classification": {"domain": "general", "confidence": 0.9},
  "responses": [...],
  "evaluations": [...],
  "comparison": {"best_model": "gpt-4-turbo-preview"}
}
```

**Errors**
- 422 validation error (missing/short prompt, no models)
- 500 internal server error

## Notes
- Send fewer models for faster responses.
- Backend reads base URL from NEXT_PUBLIC_API_URL in the frontend env.
