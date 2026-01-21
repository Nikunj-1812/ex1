"""
OpenAI Service
==============

Service for querying OpenAI models (GPT-4, GPT-3.5).

Author: MAI-PAEP Team
"""

import logging
from typing import Dict, Any, Optional
import openai
from openai import AsyncOpenAI

from app.core.config import settings

logger = logging.getLogger(__name__)


class OpenAIService:
    """
    Service for interacting with OpenAI API.
    
    Supports:
    - GPT-4 Turbo
    - GPT-3.5 Turbo
    - Token counting
    - Cost estimation
    """
    
    # Cost per 1K tokens (USD) - as of 2026
    COST_PER_1K_TOKENS = {
        "gpt-4-turbo-preview": {"input": 0.01, "output": 0.03},
        "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
    }
    
    def __init__(self):
        """Initialize OpenAI client."""
        if not settings.OPENAI_API_KEY:
            logger.warning("OpenAI API key not configured")
            self.client = None
        else:
            self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def query(
        self,
        prompt: str,
        model: str = "gpt-4-turbo-preview"
    ) -> Dict[str, Any]:
        """
        Query OpenAI model.
        
        Args:
            prompt: The prompt text
            model: Model identifier
            
        Returns:
            Response dictionary with text, tokens, and cost
            
        Raises:
            Exception: If API call fails
        """
        if not self.client:
            raise Exception("OpenAI client not initialized - check API key")
        
        try:
            # Create chat completion
            response = await self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful, accurate, and concise assistant. Provide clear, factual responses."
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
                f"OpenAI {model}: {total_tokens} tokens "
                f"(${cost:.4f})"
            )
            
            return {
                "text": text,
                "tokens": total_tokens,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cost": cost,
                "finish_reason": finish_reason,
                "version": response.model
            }
            
        except openai.RateLimitError as e:
            logger.error(f"OpenAI rate limit exceeded: {e}")
            raise Exception("Rate limit exceeded. Please try again later.")
            
        except openai.APIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise Exception(f"OpenAI API error: {str(e)}")
            
        except Exception as e:
            logger.error(f"OpenAI query failed: {e}")
            raise Exception(f"Failed to query OpenAI: {str(e)}")
    
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
        if model not in self.COST_PER_1K_TOKENS:
            logger.warning(f"Cost data not available for {model}")
            return 0.0
        
        costs = self.COST_PER_1K_TOKENS[model]
        
        input_cost = (input_tokens / 1000) * costs["input"]
        output_cost = (output_tokens / 1000) * costs["output"]
        
        return input_cost + output_cost
    
    async def count_tokens(self, text: str, model: str) -> int:
        """
        Count tokens in text (approximate).
        
        Args:
            text: Text to count tokens for
            model: Model identifier
            
        Returns:
            Approximate token count
        """
        # Rough approximation: ~4 characters per token
        return len(text) // 4
