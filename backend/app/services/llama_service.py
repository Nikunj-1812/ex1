"""
LLaMA/Mistral Service (via Groq)
=================================

Service for querying LLaMA and Mistral models via Groq API.

Author: MAI-PAEP Team
"""

import logging
from typing import Dict, Any
from groq import AsyncGroq

from app.core.config import settings

logger = logging.getLogger(__name__)


class LlamaService:
    """
    Service for interacting with LLaMA and Mistral models via Groq.
    
    Supports:
    - LLaMA 3 70B
    - LLaMA 3 8B
    - Mistral Large
    - Mixtral 8x7B
    """
    
    # Cost per 1M tokens (USD) - Groq pricing
    COST_PER_1M_TOKENS = {
        "llama-3-70b": {"input": 0.59, "output": 0.79},
        "llama-3-8b": {"input": 0.05, "output": 0.08},
        "mistral-large-latest": {"input": 0.59, "output": 0.79},
        "mixtral-8x7b": {"input": 0.27, "output": 0.27},
    }
    
    # Map our model names to Groq model IDs
    MODEL_MAP = {
        "llama-3-70b": "llama3-70b-8192",
        "llama-3-8b": "llama3-8b-8192",
        "mistral-large-latest": "mixtral-8x7b-32768",
        "mixtral-8x7b": "mixtral-8x7b-32768",
    }
    
    def __init__(self):
        """Initialize Groq client."""
        if not settings.GROQ_API_KEY:
            logger.warning("Groq API key not configured")
            self.client = None
        else:
            self.client = AsyncGroq(api_key=settings.GROQ_API_KEY)
    
    async def query(
        self,
        prompt: str,
        model: str = "llama-3-70b"
    ) -> Dict[str, Any]:
        """
        Query LLaMA/Mistral model via Groq.
        
        Args:
            prompt: The prompt text
            model: Model identifier
            
        Returns:
            Response dictionary with text, tokens, and cost
            
        Raises:
            Exception: If API call fails
        """
        if not self.client:
            raise Exception("Groq client not initialized - check API key")
        
        try:
            # Map to Groq model ID
            groq_model = self.MODEL_MAP.get(model, "llama3-70b-8192")
            
            # Create chat completion
            response = await self.client.chat.completions.create(
                model=groq_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant. Provide accurate, clear, and concise responses."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=settings.MAX_COMPLETION_TOKENS,
                temperature=0.7,
                top_p=0.9,
            )
            
            # Extract response data
            message = response.choices[0].message
            text = message.content
            finish_reason = response.choices[0].finish_reason
            
            # Token usage
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
            total_tokens = response.usage.total_tokens
            
            # Calculate cost
            cost = self._calculate_cost(model, input_tokens, output_tokens)
            
            logger.info(
                f"Groq {model}: {total_tokens} tokens "
                f"(${cost:.4f})"
            )
            
            return {
                "text": text,
                "tokens": total_tokens,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cost": cost,
                "finish_reason": finish_reason,
                "version": groq_model
            }
            
        except Exception as e:
            logger.error(f"Groq query failed: {e}")
            raise Exception(f"Failed to query Groq: {str(e)}")
    
    def _calculate_cost(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int
    ) -> float:
        """
        Calculate cost for API call.
        
        Args:
            model: Model identifier
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            
        Returns:
            Total cost in USD
        """
        if model not in self.COST_PER_1M_TOKENS:
            logger.warning(f"Cost data not available for {model}")
            return 0.0
        
        costs = self.COST_PER_1M_TOKENS[model]
        
        input_cost = (input_tokens / 1_000_000) * costs["input"]
        output_cost = (output_tokens / 1_000_000) * costs["output"]
        
        return input_cost + output_cost
