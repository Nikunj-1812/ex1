"""
Main API Router
===============

Aggregates all API endpoints.

Author: MAI-PAEP Team
"""

from fastapi import APIRouter

from app.api.v1.endpoints import prompt

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(
    prompt.router,
    prefix="/prompt",
    tags=["prompt"]
)

# Can add more routers here
# api_router.include_router(evaluation.router, prefix="/evaluation", tags=["evaluation"])
# api_router.include_router(comparison.router, prefix="/comparison", tags=["comparison"])
