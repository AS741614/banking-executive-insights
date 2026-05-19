import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.exceptions import setup_exception_handlers
from app.core.middleware import EnterpriseObservabilityMiddleware
from app.core.telemetry import setup_telemetry
from app.api.v1.router import api_router
from prometheus_client import make_asgi_app
from prometheus_fastapi_instrumentator import Instrumentator

# Initialize platform logging
setup_logging()
logger = logging.getLogger("esoteric_platform.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup Logic: Institutional Validation
    logger.info(f"Bootstrapping {settings.PROJECT_NAME} (Version: {settings.VERSION})")
    logger.info(f"Environment: {settings.ENVIRONMENT} | Debug: {settings.DEBUG}")
    
    # Boot ECOS Kernel (Adaptive Runtime)
    from ecos.main import ecos
    await ecos.boot()
    
    # Validate critical paths
    import os
    for path in [settings.DATA_DIR, settings.LOGS_DIR]:
        os.makedirs(path, exist_ok=True)
    
    logger.info("Institutional runtime validation complete. Platform ready.")
    
    yield
    
    # Shutdown Logic: Clean-up
    logger.info("Shutting down ESOTERIC Platform...")
    await ecos.shutdown()

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="Production-grade FastAPI application for the ESOTERIC BANK Intelligence Platform.",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url=f"{settings.API_V1_STR}/docs",
        redoc_url=f"{settings.API_V1_STR}/redoc",
        lifespan=lifespan
    )

    # Add Enterprise Middleware
    app.add_middleware(EnterpriseObservabilityMiddleware)

    # Initialize OpenTelemetry
    setup_telemetry(app)

    # Setup Exception Handlers
    setup_exception_handlers(app)

    # Include API Routers
    app.include_router(api_router, prefix=settings.API_V1_STR)
    
    # Prometheus Instrumentation & Metrics
    Instrumentator().instrument(app).expose(app)
    
    @app.get("/", include_in_schema=False)
    async def root():
        """Redirects root to the API documentation."""
        return RedirectResponse(url="/docs")

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
