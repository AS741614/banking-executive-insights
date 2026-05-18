import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.exceptions import setup_exception_handlers
from app.core.middleware import EnterpriseObservabilityMiddleware
from app.api.v1.router import api_router
from app.api.v1.endpoints.observability import health_check, readiness_check

# Initialize platform logging
setup_logging()
logger = logging.getLogger("esoteric_platform.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup Logic: Institutional Validation
    logger.info(f"Bootstrapping {settings.PROJECT_NAME} (Version: {settings.VERSION})")
    logger.info(f"Environment: {settings.ENVIRONMENT} | Debug: {settings.DEBUG}")
    
    # Validate critical paths
    import os
    for path in [settings.DATA_DIR, settings.LOGS_DIR]:
        os.makedirs(path, exist_ok=True)
    
    logger.info("Institutional runtime validation complete. Platform ready.")
    
    yield
    
    # Shutdown Logic: Clean-up
    logger.info("Shutting down ESOTERIC Platform...")

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="Production-grade FastAPI application for the ESOTERIC BANK Intelligence Platform.",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan
    )

    # Add Enterprise Middleware
    app.add_middleware(EnterpriseObservabilityMiddleware)

    # Setup Exception Handlers
    setup_exception_handlers(app)

    # Include API Routers
    app.include_router(api_router, prefix=settings.API_V1_STR)
    
    # Root Observability Probes
    app.add_api_route("/health", health_check, methods=["GET"], tags=["Root Observability"])
    app.add_api_route("/ready", readiness_check, methods=["GET"], tags=["Root Observability"])

    @app.get("/", include_in_schema=False)
    async def root():
        """Redirects root to the API documentation."""
        return RedirectResponse(url="/docs")

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
