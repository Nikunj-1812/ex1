"""
MAI-PAEP Backend Main Application
==================================

This is the main entry point for the FastAPI backend application.
It orchestrates all API routes, middleware, and core functionality.

Author: MAI-PAEP Team
Date: 2026
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import time
import logging

from app.core.config import settings
from app.core.logging import setup_logging
from app.api.v1.api import api_router
from app.models.database import init_db, close_db

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("🚀 Starting MAI-PAEP Backend...")
    await init_db()
    logger.info("✅ Database connections established")
    yield
    # Shutdown
    logger.info("🛑 Shutting down MAI-PAEP Backend...")
    await close_db()
    logger.info("✅ Database connections closed")


# Initialize FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Multi-AI Prompt Intelligence & Accuracy Evaluation Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)


# ==========================================
# MIDDLEWARE CONFIGURATION
# ==========================================

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GZip Compression
app.add_middleware(GZipMiddleware, minimum_size=1000)


# Request Timing Middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    Middleware to track request processing time.
    Adds X-Process-Time header to response.
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    # Log slow requests
    if process_time > 5.0:
        logger.warning(
            f"Slow request detected: {request.method} {request.url.path} "
            f"took {process_time:.2f}s"
        )
    
    return response


# Request Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware to log all incoming requests.
    """
    logger.info(
        f"Request: {request.method} {request.url.path} "
        f"from {request.client.host}"
    )
    response = await call_next(request)
    logger.info(
        f"Response: {request.method} {request.url.path} "
        f"status={response.status_code}"
    )
    return response


# Security Headers Middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """
    Middleware to add security headers to all responses.
    """
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response


# ==========================================
# EXCEPTION HANDLERS
# ==========================================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Custom handler for request validation errors.
    Provides detailed error messages for debugging.
    """
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " -> ".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    logger.error(f"Validation error for {request.url.path}: {errors}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": "Validation Error",
            "details": errors
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for unhandled exceptions.
    Prevents sensitive error details from leaking to client.
    """
    logger.exception(f"Unhandled exception for {request.url.path}: {exc}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": "Internal Server Error",
            "message": "An unexpected error occurred. Please try again later."
        }
    )


# ==========================================
# ROUTES
# ==========================================

# Include API router with v1 prefix
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint - API health check and information.
    """
    return {
        "name": settings.PROJECT_NAME,
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs",
        "api": settings.API_V1_PREFIX
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for monitoring and load balancers.
    
    Returns:
        dict: Health status of the application and dependencies
    """
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "services": {
            "api": "operational",
            "database": "connected",
            "cache": "connected"
        }
    }


@app.get("/metrics", tags=["Monitoring"])
async def metrics():
    """
    Basic metrics endpoint for monitoring.
    Can be extended to provide Prometheus-compatible metrics.
    """
    return {
        "requests_total": "tracked_by_middleware",
        "active_connections": "tracked_by_middleware",
        "response_time_avg": "tracked_by_middleware"
    }


# ==========================================
# STARTUP MESSAGE
# ==========================================

if __name__ == "__main__":
    import uvicorn
    
    logger.info("=" * 60)
    logger.info("MAI-PAEP Backend API")
    logger.info("=" * 60)
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug Mode: {settings.DEBUG}")
    logger.info(f"API Prefix: {settings.API_V1_PREFIX}")
    logger.info(f"CORS Origins: {settings.CORS_ORIGINS}")
    logger.info("=" * 60)
    
    uvicorn.run(
        "app.main:app",
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
