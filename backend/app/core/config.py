"""
Configuration Settings
======================

Centralized configuration management using Pydantic Settings.
All environment variables are loaded and validated here.

Author: MAI-PAEP Team
"""

from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import List, Optional
import secrets


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    
    # ==========================================
    # PROJECT SETTINGS
    # ==========================================
    PROJECT_NAME: str = "MAI-PAEP"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    DEBUG: bool = Field(default=False, env="DEBUG")
    
    # ==========================================
    # API SETTINGS
    # ==========================================
    API_V1_PREFIX: str = "/api/v1"
    BACKEND_HOST: str = Field(default="0.0.0.0", env="BACKEND_HOST")
    BACKEND_PORT: int = Field(default=8000, env="BACKEND_PORT")
    BACKEND_URL: str = Field(default="http://localhost:8000", env="BACKEND_URL")
    FRONTEND_URL: str = Field(default="http://localhost:3000", env="FRONTEND_URL")
    
    # ==========================================
    # SECURITY
    # ==========================================
    SECRET_KEY: str = Field(default_factory=lambda: secrets.token_urlsafe(32))
    JWT_SECRET: str = Field(default_factory=lambda: secrets.token_urlsafe(32))
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    ENCRYPTION_KEY: str = Field(default_factory=lambda: secrets.token_urlsafe(32))
    
    # ==========================================
    # CORS
    # ==========================================
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:3001"],
        env="CORS_ORIGINS"
    )
    
    @validator("CORS_ORIGINS", pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    # ==========================================
    # DATABASE - POSTGRESQL
    # ==========================================
    POSTGRES_HOST: str = Field(default="localhost", env="POSTGRES_HOST")
    POSTGRES_PORT: int = Field(default=5432, env="POSTGRES_PORT")
    POSTGRES_DB: str = Field(default="maipaep", env="POSTGRES_DB")
    POSTGRES_USER: str = Field(default="maipaep_user", env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(default="password", env="POSTGRES_PASSWORD")
    
    @property
    def POSTGRES_URL(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
    
    # ==========================================
    # DATABASE - MONGODB
    # ==========================================
    MONGODB_HOST: str = Field(default="localhost", env="MONGODB_HOST")
    MONGODB_PORT: int = Field(default=27017, env="MONGODB_PORT")
    MONGODB_DB: str = Field(default="maipaep", env="MONGODB_DB")
    MONGODB_USER: Optional[str] = Field(default=None, env="MONGODB_USER")
    MONGODB_PASSWORD: Optional[str] = Field(default=None, env="MONGODB_PASSWORD")
    
    @property
    def MONGODB_URL(self) -> str:
        if self.MONGODB_USER and self.MONGODB_PASSWORD:
            return (
                f"mongodb://{self.MONGODB_USER}:{self.MONGODB_PASSWORD}"
                f"@{self.MONGODB_HOST}:{self.MONGODB_PORT}/{self.MONGODB_DB}"
            )
        return f"mongodb://{self.MONGODB_HOST}:{self.MONGODB_PORT}/{self.MONGODB_DB}"
    
    # ==========================================
    # REDIS (CACHE)
    # ==========================================
    REDIS_HOST: str = Field(default="localhost", env="REDIS_HOST")
    REDIS_PORT: int = Field(default=6379, env="REDIS_PORT")
    REDIS_DB: int = Field(default=0, env="REDIS_DB")
    REDIS_PASSWORD: Optional[str] = Field(default=None, env="REDIS_PASSWORD")
    
    @property
    def REDIS_URL(self) -> str:
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    # ==========================================
    # AI API KEYS
    # ==========================================
    OPENAI_API_KEY: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")
    GOOGLE_API_KEY: Optional[str] = Field(default=None, env="GOOGLE_API_KEY")
    GROQ_API_KEY: Optional[str] = Field(default=None, env="GROQ_API_KEY")
    HUGGINGFACE_API_KEY: Optional[str] = Field(default=None, env="HUGGINGFACE_API_KEY")
    MISTRAL_API_KEY: Optional[str] = Field(default=None, env="MISTRAL_API_KEY")
    
    # ==========================================
    # AI MODEL CONFIGURATION
    # ==========================================
    DEFAULT_GPT_MODEL: str = "gpt-4-turbo-preview"
    DEFAULT_CLAUDE_MODEL: str = "claude-3-opus-20240229"
    DEFAULT_GEMINI_MODEL: str = "gemini-pro"
    DEFAULT_LLAMA_MODEL: str = "llama-3-70b"
    DEFAULT_MISTRAL_MODEL: str = "mistral-large-latest"
    
    AI_REQUEST_TIMEOUT: int = Field(default=60, env="AI_REQUEST_TIMEOUT")
    AI_MAX_RETRIES: int = Field(default=3, env="AI_MAX_RETRIES")
    MAX_PROMPT_TOKENS: int = Field(default=4000, env="MAX_PROMPT_TOKENS")
    MAX_COMPLETION_TOKENS: int = Field(default=2000, env="MAX_COMPLETION_TOKENS")
    
    # ==========================================
    # ML MODEL CONFIGURATION
    # ==========================================
    SBERT_MODEL: str = Field(default="all-MiniLM-L6-v2", env="SBERT_MODEL")
    DOMAIN_CLASSIFIER_MODEL: str = Field(default="bert-base-uncased", env="DOMAIN_CLASSIFIER_MODEL")
    ML_DEVICE: str = Field(default="cpu", env="ML_DEVICE")
    ML_BATCH_SIZE: int = Field(default=32, env="ML_BATCH_SIZE")
    
    # ==========================================
    # CACHING
    # ==========================================
    CACHE_ENABLED: bool = Field(default=True, env="CACHE_ENABLED")
    CACHE_TTL_SECONDS: int = Field(default=300, env="CACHE_TTL_SECONDS")
    CACHE_AI_RESPONSES: bool = Field(default=True, env="CACHE_AI_RESPONSES")
    CACHE_EVALUATIONS: bool = Field(default=True, env="CACHE_EVALUATIONS")
    
    # ==========================================
    # RATE LIMITING
    # ==========================================
    RATE_LIMIT_ENABLED: bool = Field(default=True, env="RATE_LIMIT_ENABLED")
    RATE_LIMIT_PER_MINUTE: int = Field(default=60, env="RATE_LIMIT_PER_MINUTE")
    RATE_LIMIT_PER_HOUR: int = Field(default=1000, env="RATE_LIMIT_PER_HOUR")
    RATE_LIMIT_PER_DAY: int = Field(default=10000, env="RATE_LIMIT_PER_DAY")
    
    # ==========================================
    # LOGGING
    # ==========================================
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FORMAT: str = Field(default="json", env="LOG_FORMAT")
    LOG_FILE_PATH: str = Field(default="./logs/app.log", env="LOG_FILE_PATH")
    
    # ==========================================
    # FEATURE FLAGS
    # ==========================================
    ENABLE_WEBSOCKETS: bool = Field(default=True, env="ENABLE_WEBSOCKETS")
    ENABLE_REAL_TIME_UPDATES: bool = Field(default=True, env="ENABLE_REAL_TIME_UPDATES")
    ENABLE_BIAS_DETECTION: bool = Field(default=True, env="ENABLE_BIAS_DETECTION")
    ENABLE_HALLUCINATION_DETECTION: bool = Field(default=True, env="ENABLE_HALLUCINATION_DETECTION")
    ENABLE_DOMAIN_CLASSIFICATION: bool = Field(default=True, env="ENABLE_DOMAIN_CLASSIFICATION")
    ENABLE_SAFETY_WARNINGS: bool = Field(default=True, env="ENABLE_SAFETY_WARNINGS")
    
    # ==========================================
    # RESEARCH & ANALYTICS
    # ==========================================
    SAVE_ALL_PROMPTS: bool = Field(default=True, env="SAVE_ALL_PROMPTS")
    SAVE_ALL_RESPONSES: bool = Field(default=True, env="SAVE_ALL_RESPONSES")
    ENABLE_ANALYTICS: bool = Field(default=True, env="ENABLE_ANALYTICS")
    ANONYMIZE_DATA: bool = Field(default=True, env="ANONYMIZE_DATA")
    
    # ==========================================
    # VECTOR DATABASE
    # ==========================================
    FAISS_INDEX_PATH: str = Field(default="./ml/models/faiss_index", env="FAISS_INDEX_PATH")
    PINECONE_API_KEY: Optional[str] = Field(default=None, env="PINECONE_API_KEY")
    PINECONE_ENVIRONMENT: Optional[str] = Field(default=None, env="PINECONE_ENVIRONMENT")
    PINECONE_INDEX_NAME: str = Field(default="maipaep-vectors", env="PINECONE_INDEX_NAME")
    
    # ==========================================
    # MONITORING
    # ==========================================
    ENABLE_METRICS: bool = Field(default=True, env="ENABLE_METRICS")
    SENTRY_DSN: Optional[str] = Field(default=None, env="SENTRY_DSN")
    SENTRY_ENVIRONMENT: str = Field(default="development", env="SENTRY_ENVIRONMENT")
    
    # ==========================================
    # COST TRACKING
    # ==========================================
    ENABLE_COST_TRACKING: bool = Field(default=True, env="ENABLE_COST_TRACKING")
    MONTHLY_BUDGET_USD: float = Field(default=1000.0, env="MONTHLY_BUDGET_USD")
    ALERT_THRESHOLD_PERCENT: float = Field(default=80.0, env="ALERT_THRESHOLD_PERCENT")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()
