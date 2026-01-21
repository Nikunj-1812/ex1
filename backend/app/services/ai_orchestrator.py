"""
AI Orchestration Service
=========================

Coordinates simultaneous queries to multiple AI models.
Handles failures, timeouts, and response collection.

Author: MAI-PAEP Team
"""

import asyncio
import logging
import time
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

from app.core.config import settings
from app.services.openai_service import OpenAIService
from app.services.anthropic_service import AnthropicService
from app.services.google_service import GoogleService
from app.services.llama_service import LlamaService
from app.models.database import get_redis

logger = logging.getLogger(__name__)


class AIOrchestrator:
    """
    Orchestrates queries to multiple AI models simultaneously.
    
    Responsibilities:
    - Normalize prompts
    - Dispatch to selected AI services
    - Handle timeouts and errors gracefully
    - Track latency per model
    - Implement caching strategy
    - Cost optimization
    """
    
    def __init__(self):
        """Initialize AI service clients."""
        self.openai_service = OpenAIService()
        self.anthropic_service = AnthropicService()
        self.google_service = GoogleService()
        self.llama_service = LlamaService()
        
        # Map model names to services
        self.service_map = {
            "gpt-4-turbo-preview": self.openai_service,
            "gpt-3.5-turbo": self.openai_service,
            "claude-3-opus-20240229": self.anthropic_service,
            "claude-3-sonnet-20240229": self.anthropic_service,
            "gemini-pro": self.google_service,
            "llama-3-70b": self.llama_service,
            "mistral-large-latest": self.llama_service,  # Via Groq
        }
    
    async def query_models(
        self,
        prompt: str,
        selected_models: List[str],
        session_id: str
    ) -> List[Dict[str, Any]]:
        """
        Query multiple AI models concurrently.
        
        Args:
            prompt: The normalized prompt text
            selected_models: List of model identifiers
            session_id: Session identifier for tracking
            
        Returns:
            List of response dictionaries with metadata
        """
        logger.info(f"Session {session_id}: Querying {len(selected_models)} models")
        
        # Check cache first
        cached_responses = await self._check_cache(prompt, selected_models)
        
        # Create tasks for uncached models
        tasks = []
        for model in selected_models:
            if model in cached_responses:
                continue
            
            task = self._query_single_model(prompt, model, session_id)
            tasks.append(task)
        
        # Execute all queries concurrently with timeout
        if tasks:
            try:
                responses = await asyncio.gather(*tasks, return_exceptions=True)
            except Exception as e:
                logger.error(f"Error in concurrent queries: {e}")
                responses = []
        else:
            responses = []
        
        # Combine cached and new responses
        all_responses = list(cached_responses.values())
        
        for response in responses:
            if isinstance(response, Exception):
                logger.error(f"Query failed: {response}")
                continue
            
            if response:
                all_responses.append(response)
                
                # Cache successful responses
                if settings.CACHE_AI_RESPONSES:
                    await self._cache_response(prompt, response)
        
        logger.info(
            f"Session {session_id}: Received {len(all_responses)} responses"
        )
        
        return all_responses
    
    async def _query_single_model(
        self,
        prompt: str,
        model: str,
        session_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Query a single AI model with timeout and error handling.
        
        Args:
            prompt: The prompt text
            model: Model identifier
            session_id: Session identifier
            
        Returns:
            Response dictionary or None on failure
        """
        start_time = time.time()
        response_id = f"resp_{uuid.uuid4().hex[:12]}"
        
        try:
            # Get appropriate service
            service = self.service_map.get(model)
            
            if not service:
                logger.error(f"No service found for model: {model}")
                return self._create_error_response(
                    response_id, session_id, model,
                    "Service not available", 0
                )
            
            # Query with timeout
            response_data = await asyncio.wait_for(
                service.query(prompt, model),
                timeout=settings.AI_REQUEST_TIMEOUT
            )
            
            # Calculate latency
            latency_ms = (time.time() - start_time) * 1000
            
            # Build response object
            response = {
                "response_id": response_id,
                "session_id": session_id,
                "model_name": model,
                "model_provider": self._get_provider(model),
                "response_text": response_data.get("text", ""),
                "response_length": len(response_data.get("text", "")),
                "latency_ms": latency_ms,
                "tokens_used": response_data.get("tokens", 0),
                "estimated_cost": response_data.get("cost", 0.0),
                "status": "success",
                "error_message": None,
                "created_at": datetime.utcnow(),
                "api_version": response_data.get("version"),
                "finish_reason": response_data.get("finish_reason", "stop")
            }
            
            logger.info(
                f"Model {model} responded in {latency_ms:.2f}ms "
                f"({response['tokens_used']} tokens)"
            )
            
            return response
            
        except asyncio.TimeoutError:
            latency_ms = (time.time() - start_time) * 1000
            logger.warning(f"Model {model} timed out after {latency_ms:.2f}ms")
            
            return self._create_error_response(
                response_id, session_id, model,
                "Request timed out", latency_ms
            )
            
        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            logger.error(f"Model {model} failed: {e}")
            
            return self._create_error_response(
                response_id, session_id, model,
                str(e), latency_ms
            )
    
    def _create_error_response(
        self,
        response_id: str,
        session_id: str,
        model: str,
        error: str,
        latency_ms: float
    ) -> Dict[str, Any]:
        """Create an error response object."""
        return {
            "response_id": response_id,
            "session_id": session_id,
            "model_name": model,
            "model_provider": self._get_provider(model),
            "response_text": "",
            "response_length": 0,
            "latency_ms": latency_ms,
            "tokens_used": 0,
            "estimated_cost": 0.0,
            "status": "error",
            "error_message": error,
            "created_at": datetime.utcnow(),
            "api_version": None,
            "finish_reason": "error"
        }
    
    def _get_provider(self, model: str) -> str:
        """Get provider name from model identifier."""
        if "gpt" in model.lower():
            return "openai"
        elif "claude" in model.lower():
            return "anthropic"
        elif "gemini" in model.lower():
            return "google"
        elif "llama" in model.lower():
            return "meta"
        elif "mistral" in model.lower():
            return "mistral"
        return "unknown"
    
    async def _check_cache(
        self,
        prompt: str,
        models: List[str]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Check Redis cache for existing responses.
        
        Args:
            prompt: The prompt text
            models: List of model identifiers
            
        Returns:
            Dictionary of cached responses by model
        """
        if not settings.CACHE_ENABLED or not settings.CACHE_AI_RESPONSES:
            return {}
        
        try:
            redis = get_redis()
            if not redis:
                return {}
            
            cached = {}
            
            for model in models:
                cache_key = f"response:{hash(prompt)}:{model}"
                cached_data = await redis.get(cache_key)
                
                if cached_data:
                    import json
                    cached[model] = json.loads(cached_data)
                    logger.info(f"Cache hit for model {model}")
            
            return cached
            
        except Exception as e:
            logger.error(f"Cache check failed: {e}")
            return {}
    
    async def _cache_response(
        self,
        prompt: str,
        response: Dict[str, Any]
    ):
        """
        Cache a successful response.
        
        Args:
            prompt: The prompt text
            response: Response dictionary to cache
        """
        if not settings.CACHE_ENABLED or not settings.CACHE_AI_RESPONSES:
            return
        
        try:
            redis = get_redis()
            if not redis:
                return
            
            model = response["model_name"]
            cache_key = f"response:{hash(prompt)}:{model}"
            
            import json
            await redis.setex(
                cache_key,
                settings.CACHE_TTL_SECONDS,
                json.dumps(response, default=str)
            )
            
            logger.info(f"Cached response for model {model}")
            
        except Exception as e:
            logger.error(f"Cache write failed: {e}")
    
    def normalize_prompt(self, prompt: str) -> str:
        """
        Normalize prompt text for consistent processing.
        
        Args:
            prompt: Raw prompt text
            
        Returns:
            Normalized prompt
        """
        # Remove extra whitespace
        normalized = " ".join(prompt.split())
        
        # Trim to max length
        if len(normalized) > settings.MAX_PROMPT_TOKENS * 4:  # ~4 chars per token
            normalized = normalized[:settings.MAX_PROMPT_TOKENS * 4]
        
        return normalized
