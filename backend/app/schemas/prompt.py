"""
Pydantic Schemas for Prompt and Response
=========================================

Request and response models for API validation.

Author: MAI-PAEP Team
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class AIModel(str, Enum):
    """Available AI models for selection."""
    GPT4 = "gpt-4-turbo-preview"
    GPT35 = "gpt-3.5-turbo"
    CLAUDE3_OPUS = "claude-3-opus-20240229"
    CLAUDE3_SONNET = "claude-3-sonnet-20240229"
    GEMINI_PRO = "gemini-pro"
    LLAMA3_70B = "llama-3-70b"
    MISTRAL_LARGE = "mistral-large-latest"


class Domain(str, Enum):
    """Problem domain classifications."""
    MEDICAL = "medical"
    LEGAL = "legal"
    CODING = "coding"
    EDUCATION = "education"
    BUSINESS = "business"
    MENTAL_HEALTH = "mental_health"
    GENERAL = "general"


class SafetyLevel(str, Enum):
    """Safety level classifications."""
    SAFE = "safe"
    WARNING = "warning"
    CRITICAL = "critical"


# ==========================================
# REQUEST SCHEMAS
# ==========================================

class PromptSubmitRequest(BaseModel):
    """
    Request schema for submitting a prompt for evaluation.
    """
    prompt: str = Field(
        ...,
        min_length=10,
        max_length=4000,
        description="The prompt text to evaluate"
    )
    
    selected_models: List[AIModel] = Field(
        ...,
        min_items=2,
        max_items=7,
        description="List of AI models to query (minimum 2)"
    )
    
    user_id: Optional[str] = Field(
        None,
        description="Optional user identifier"
    )
    
    @validator("prompt")
    def validate_prompt(cls, v):
        """Validate prompt is not empty or just whitespace."""
        if not v.strip():
            raise ValueError("Prompt cannot be empty")
        return v.strip()
    
    @validator("selected_models")
    def validate_unique_models(cls, v):
        """Ensure no duplicate models selected."""
        if len(v) != len(set(v)):
            raise ValueError("Duplicate models not allowed")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "prompt": "What are the symptoms of type 2 diabetes?",
                "selected_models": ["gpt-4-turbo-preview", "claude-3-opus-20240229", "gemini-pro"],
                "user_id": "user123"
            }
        }


class FeedbackRequest(BaseModel):
    """
    Request schema for submitting user feedback.
    """
    session_id: str
    response_id: Optional[str] = None
    rating: int = Field(..., ge=1, le=5, description="Rating from 1-5 stars")
    was_helpful: bool
    was_accurate: bool
    comment: Optional[str] = Field(None, max_length=1000)
    preferred_model: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "session_id": "sess_abc123",
                "response_id": "resp_xyz789",
                "rating": 5,
                "was_helpful": True,
                "was_accurate": True,
                "comment": "Very helpful and accurate response!",
                "preferred_model": "gpt-4-turbo-preview"
            }
        }


# ==========================================
# RESPONSE SCHEMAS
# ==========================================

class AIResponseSchema(BaseModel):
    """
    Schema for individual AI model response.
    """
    response_id: str
    model_name: str
    model_provider: str
    response_text: str
    response_length: int
    latency_ms: float
    tokens_used: Optional[int] = None
    estimated_cost: Optional[float] = None
    status: str
    error_message: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class EvaluationScores(BaseModel):
    """
    Evaluation scores for a response.
    """
    relevance_score: float = Field(..., ge=0, le=100)
    accuracy_score: float = Field(..., ge=0, le=100)
    clarity_score: float = Field(..., ge=0, le=100)
    hallucination_risk: float = Field(..., ge=0, le=100)
    bias_score: float = Field(..., ge=0, le=100)
    trust_score: float = Field(..., ge=0, le=100)
    
    semantic_similarity: Optional[float] = None
    readability_metrics: Optional[Dict[str, Any]] = None
    coherence_metrics: Optional[Dict[str, Any]] = None
    
    rank_by_relevance: Optional[int] = None
    rank_by_trust: Optional[int] = None
    is_best_overall: bool = False
    is_safest: bool = False
    
    recommendation: Optional[str] = None
    warnings: List[str] = []


class EvaluationResultSchema(BaseModel):
    """
    Complete evaluation result for a response.
    """
    evaluation_id: str
    response_id: str
    response: AIResponseSchema
    scores: EvaluationScores
    
    class Config:
        from_attributes = True


class DomainClassification(BaseModel):
    """
    Domain classification result.
    """
    domain: Domain
    confidence: float = Field(..., ge=0, le=1)
    is_sensitive: bool
    safety_level: SafetyLevel
    warnings: List[str] = []
    recommendations: List[str] = []


class ComparisonResult(BaseModel):
    """
    Comparison result showing best AI and answer.
    """
    best_model: str
    best_model_reason: str
    best_answer: str
    safest_model: str
    safest_answer: str
    
    ranking_by_trust: List[Dict[str, Any]]
    ranking_by_relevance: List[Dict[str, Any]]
    
    cost_analysis: Dict[str, Any]
    performance_analysis: Dict[str, Any]


class PromptSubmitResponse(BaseModel):
    """
    Response schema for prompt submission.
    """
    success: bool
    session_id: str
    message: str
    
    # Domain classification
    domain_classification: DomainClassification
    
    # AI responses
    responses: List[AIResponseSchema]
    
    # Evaluations
    evaluations: List[EvaluationResultSchema]
    
    # Comparison
    comparison: ComparisonResult
    
    # Metadata
    total_latency_ms: float
    total_cost: float
    timestamp: datetime
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "session_id": "sess_abc123",
                "message": "Evaluation completed successfully",
                "domain_classification": {
                    "domain": "medical",
                    "confidence": 0.95,
                    "is_sensitive": True,
                    "safety_level": "warning",
                    "warnings": ["Medical information should be verified with healthcare professional"],
                    "recommendations": ["Consult with a doctor for personalized advice"]
                },
                "responses": [],
                "evaluations": [],
                "comparison": {
                    "best_model": "gpt-4-turbo-preview",
                    "best_model_reason": "Highest trust score with balanced accuracy and clarity",
                    "best_answer": "...",
                    "safest_model": "claude-3-opus-20240229",
                    "safest_answer": "...",
                    "ranking_by_trust": [],
                    "ranking_by_relevance": [],
                    "cost_analysis": {},
                    "performance_analysis": {}
                },
                "total_latency_ms": 2543.5,
                "total_cost": 0.0234,
                "timestamp": "2026-01-20T10:30:00Z"
            }
        }


class ErrorResponse(BaseModel):
    """
    Standard error response.
    """
    success: bool = False
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None


class HealthResponse(BaseModel):
    """
    Health check response.
    """
    status: str
    timestamp: float
    services: Dict[str, str]
