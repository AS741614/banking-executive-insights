from fastapi import APIRouter

from app.api.v1.endpoints import cognition, observability, executive, regulatory

api_router = APIRouter()

# Group observability endpoints
api_router.include_router(observability.router, prefix="/platform", tags=["Platform"])
api_router.include_router(observability.router, prefix="/observability", tags=["Observability"])

# Regulatory Cognition Domain
api_router.include_router(regulatory.router, prefix="/regulatory", tags=["Regulatory"])

# To satisfy the exact root endpoints required like /health, we can also map them directly in main.py,
# but for modularity, let's include them here and handle root in main.py if needed.
api_router.include_router(cognition.router, prefix="/cognition", tags=["Cognition"])

# Include the rest under a general tag or individually.
api_router.include_router(executive.router, tags=["Enterprise Domains"])