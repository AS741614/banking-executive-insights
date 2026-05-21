import logging
import os
import socket
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from app.core.config import settings

logger = logging.getLogger("esoteric_bank.core.telemetry")

def is_running_in_docker():
    """Simple check to determine if the application is running inside a container."""
    path = '/proc/self/cgroup'
    return (
        os.path.exists('/.dockerenv') or
        os.path.isfile(path) and any('docker' in line for line in open(path))
    )

def setup_telemetry(app):
    """
    Sets up OpenTelemetry tracing for the FastAPI application with institutional-grade
    resilience and environment-aware configuration.
    """
    if not settings.PROMETHEUS_METRICS_ENABLED:
        logger.info("Telemetry is disabled via configuration.")
        return

    # 1. Environment Detection & Endpoint Resolution
    is_docker = is_running_in_docker()
    
    # Check if we can reach the docker-internal hostname, otherwise fallback to localhost
    otel_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    
    if not otel_endpoint:
        if is_docker:
            otel_endpoint = "http://otel-collector:4317"
            logger.info(f"Docker environment detected. Targeting OTEL collector at {otel_endpoint}")
        else:
            otel_endpoint = "http://localhost:4317"
            logger.info(f"Local environment detected. Targeting OTEL collector at {otel_endpoint}")

    # 2. Resource Definition
    resource = Resource.create({
        "service.name": settings.PROJECT_NAME,
        "service.version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "runtime.mode": "docker" if is_docker else "local"
    })

    # 3. Tracer Provider Initialization
    provider = TracerProvider(resource=resource)
    
    # 4. Resilient Exporter Provisioning
    try:
        # We use a short timeout for the initial connection attempt to prevent startup hangs
        otlp_exporter = OTLPSpanExporter(endpoint=otel_endpoint, insecure=True, timeout=5)
        processor = BatchSpanProcessor(otlp_exporter)
        provider.add_span_processor(processor)
        logger.info(f"OTEL OTLP Exporter activated: {otel_endpoint}")
    except Exception as e:
        # Graceful degradation: If the collector is missing, we proceed without export
        # This prevents the 'UNAVAILABLE' warning spam from crashing or slowing the kernel
        logger.warning(f"OTEL Collector unreachable at {otel_endpoint}. Tracing will be recorded locally but not exported. Reason: {e}")

    trace.set_tracer_provider(provider)

    # 5. Institutional Instrumentation
    FastAPIInstrumentor.instrument_app(app)
    
    logger.info("Institutional telemetry reconciliation complete.")

