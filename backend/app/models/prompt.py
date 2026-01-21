"""
Prompt Database Models
======================

SQLAlchemy models for storing prompts and related data.

Author: MAI-PAEP Team
"""

from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from datetime import datetime

from app.models.database import Base


class PromptSession(Base):
    """
    Stores information about each prompt evaluation session.
    """
    __tablename__ = "prompt_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(255), unique=True, nullable=False, index=True)
    
    # Prompt information
    prompt_text = Column(Text, nullable=False)
    prompt_length = Column(Integer)
    
    # Classification
    domain = Column(String(100))  # medical, legal, coding, etc.
    is_sensitive = Column(Boolean, default=False)
    safety_level = Column(String(50))  # safe, warning, critical
    
    # Selected models
    selected_models = Column(JSON)  # List of AI models used
    
    # Metadata
    user_id = Column(String(255), nullable=True)  # Optional user tracking
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(500), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Status
    status = Column(String(50), default="pending")  # pending, processing, completed, failed
    
    def __repr__(self):
        return f"<PromptSession {self.session_id}>"


class AIResponse(Base):
    """
    Stores individual AI model responses.
    """
    __tablename__ = "ai_responses"
    
    id = Column(Integer, primary_key=True, index=True)
    response_id = Column(String(255), unique=True, nullable=False, index=True)
    session_id = Column(String(255), nullable=False, index=True)
    
    # Model information
    model_name = Column(String(100), nullable=False)  # gpt-4, claude-3, etc.
    model_provider = Column(String(50))  # openai, anthropic, google, etc.
    
    # Response data
    response_text = Column(Text, nullable=False)
    response_length = Column(Integer)
    
    # Performance metrics
    latency_ms = Column(Float)  # Response time in milliseconds
    tokens_used = Column(Integer)
    estimated_cost = Column(Float)
    
    # API metadata
    api_version = Column(String(50))
    finish_reason = Column(String(50))  # stop, length, content_filter, etc.
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Status
    status = Column(String(50), default="success")  # success, error, timeout
    error_message = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<AIResponse {self.response_id} - {self.model_name}>"


class EvaluationResult(Base):
    """
    Stores evaluation results for each AI response.
    """
    __tablename__ = "evaluation_results"
    
    id = Column(Integer, primary_key=True, index=True)
    evaluation_id = Column(String(255), unique=True, nullable=False, index=True)
    response_id = Column(String(255), nullable=False, index=True)
    session_id = Column(String(255), nullable=False, index=True)
    
    # Core evaluation scores (0-100)
    relevance_score = Column(Float, nullable=False)
    accuracy_score = Column(Float, nullable=False)
    clarity_score = Column(Float, nullable=False)
    
    # Risk metrics (0-100)
    hallucination_risk = Column(Float, nullable=False)
    bias_score = Column(Float, nullable=False)
    
    # Composite scores
    trust_score = Column(Float, nullable=False)  # Weighted average
    
    # Detailed metrics (stored as JSON)
    semantic_similarity = Column(Float)
    readability_metrics = Column(JSON)  # Flesch score, etc.
    coherence_metrics = Column(JSON)
    factual_consistency = Column(JSON)
    bias_analysis = Column(JSON)
    
    # Rankings
    rank_by_relevance = Column(Integer)
    rank_by_trust = Column(Integer)
    is_best_overall = Column(Boolean, default=False)
    is_safest = Column(Boolean, default=False)
    
    # Recommendations
    recommendation = Column(Text)
    warnings = Column(JSON)  # List of warnings
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<EvaluationResult {self.evaluation_id}>"


class UserFeedback(Base):
    """
    Stores user feedback for reinforcement learning.
    """
    __tablename__ = "user_feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    feedback_id = Column(String(255), unique=True, nullable=False, index=True)
    session_id = Column(String(255), nullable=False, index=True)
    response_id = Column(String(255), nullable=True, index=True)
    
    # Feedback data
    rating = Column(Integer)  # 1-5 stars
    was_helpful = Column(Boolean)
    was_accurate = Column(Boolean)
    
    # User comments
    comment = Column(Text, nullable=True)
    
    # Preferred response
    preferred_model = Column(String(100), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<UserFeedback {self.feedback_id}>"


class CostTracking(Base):
    """
    Tracks API costs for budget management.
    """
    __tablename__ = "cost_tracking"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(255), nullable=False, index=True)
    
    # Cost breakdown
    model_name = Column(String(100), nullable=False)
    input_tokens = Column(Integer)
    output_tokens = Column(Integer)
    total_tokens = Column(Integer)
    
    # Costs in USD
    input_cost = Column(Float)
    output_cost = Column(Float)
    total_cost = Column(Float)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<CostTracking {self.model_name} - ${self.total_cost}>"
