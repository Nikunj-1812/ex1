"""
Anthropic Service
=================

Service for querying Anthropic models (Claude).

Author: MAI-PAEP Team
"""

import logging
from typing import Dict, Any
from anthropic import AsyncAnthropic

from app.core.config import settings

logger = logging.getLogger(__name__)


class AnthropicService:
    """
    Service for interacting with Anthropic API.
    
    Supports:
    - Claude 3 Opus
    - Claude 3 Sonnet
    - Claude 3 Haiku
    """
    
    # Cost per 1M tokens (USD) - as of 2026
    COST_PER_1M_TOKENS = {
        "claude-3-opus-20240229": {"input": 15.0, "output": 75.0},
        "claude-3-sonnet-20240229": {"input": 3.0, "output": 15.0},
        "claude-3-haiku-20240307": {"input": 0.25, "output": 1.25},
    }
    
    def __init__(self):
        """Initialize Anthropic client."""
        if not settings.ANTHROPIC_API_KEY:
            logger.warning("Anthropic API key not configured")
            self.client = None
        else:
            self.client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
    
    async def query(
        self,
        prompt: str,
        model: str = "claude-3-opus-20240229"
    ) -> Dict[str, Any]:
        """
        Query Anthropic Claude model.
        
        Args:
            prompt: The prompt text
            model: Model identifier
            
        Returns:
            Response dictionary with text, tokens, and cost
            
        Raises:
            Exception: If API call fails
        """
        if not self.client:
            raise Exception("Anthropic client not initialized - check API key")
        
        try:
            # Create message
            response = await self.client.messages.create(
                model=model,
                max_tokens=settings.MAX_COMPLETION_TOKENS,
                temperature=0.7,
                system="You are a helpful, accurate, and thoughtful assistant. Provide clear, well-reasoned responses.",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # Extract response data
            text = response.content[0].text
            finish_reason = response.stop_reason
            
            # Token usage
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
            total_tokens = input_tokens + output_tokens
            
            # Calculate cost
            cost = self._calculate_cost(model, input_tokens, output_tokens)
            
            logger.info(
                f"Anthropic {model}: {total_tokens} tokens "
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
            
        except Exception as e:
            logger.error(f"Anthropic query failed: {e}")
            raise Exception(f"Failed to query Anthropic: {str(e)}")
    
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
