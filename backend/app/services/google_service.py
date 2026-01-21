"""
Google AI Service
=================

Service for querying Google AI models (Gemini).

Author: MAI-PAEP Team
"""

import logging
from typing import Dict, Any
import google.generativeai as genai

from app.core.config import settings

logger = logging.getLogger(__name__)


class GoogleService:
    """
    Service for interacting with Google AI API.
    
    Supports:
    - Gemini Pro
    - Gemini Pro Vision
    """
    
    # Cost per 1M tokens (USD) - as of 2026
    COST_PER_1M_TOKENS = {
        "gemini-pro": {"input": 0.5, "output": 1.5},
        "gemini-pro-vision": {"input": 0.5, "output": 1.5},
    }
    
    def __init__(self):
        """Initialize Google AI client."""
        if not settings.GOOGLE_API_KEY:
            logger.warning("Google API key not configured")
            self.client = None
        else:
            genai.configure(api_key=settings.GOOGLE_API_KEY)
            self.client = True
    
    async def query(
        self,
        prompt: str,
        model: str = "gemini-pro"
    ) -> Dict[str, Any]:
        """
        Query Google Gemini model.
        
        Args:
            prompt: The prompt text
            model: Model identifier
            
        Returns:
            Response dictionary with text, tokens, and cost
            
        Raises:
            Exception: If API call fails
        """
        if not self.client:
            raise Exception("Google AI client not initialized - check API key")
        
        try:
            # Initialize model
            gemini_model = genai.GenerativeModel(model)
            
            # Generate content
            response = await gemini_model.generate_content_async(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=settings.MAX_COMPLETION_TOKENS,
                    temperature=0.7,
                    top_p=0.9,
                )
            )
            
            # Extract response data
            text = response.text
            finish_reason = str(response.candidates[0].finish_reason) if response.candidates else "STOP"
            
            # Estimate tokens (Gemini doesn't always provide exact counts)
            input_tokens = len(prompt) // 4  # Rough estimate
            output_tokens = len(text) // 4  # Rough estimate
            total_tokens = input_tokens + output_tokens
            
            # Try to get actual token counts if available
            try:
                if hasattr(response, 'usage_metadata'):
                    input_tokens = response.usage_metadata.prompt_token_count
                    output_tokens = response.usage_metadata.candidates_token_count
                    total_tokens = response.usage_metadata.total_token_count
            except:
                pass
            
            # Calculate cost
            cost = self._calculate_cost(model, input_tokens, output_tokens)
            
            logger.info(
                f"Google {model}: {total_tokens} tokens "
                f"(${cost:.4f})"
            )
            
            return {
                "text": text,
                "tokens": total_tokens,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cost": cost,
                "finish_reason": finish_reason,
                "version": model
            }
            
        except Exception as e:
            logger.error(f"Google AI query failed: {e}")
            raise Exception(f"Failed to query Google AI: {str(e)}")
    
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
