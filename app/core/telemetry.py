import logging
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from app.core.config import settings

logger = logging.getLogger("esoteric_bank.core.telemetry")

def setup_telemetry(app):
    """
    Sets up OpenTelemetry tracing for the FastAPI application.
    """
    if not settings.PROMETHEUS_METRICS_ENABLED:
        logger.info("Telemetry is disabled via configuration.")
        return

    logger.info("Initializing OpenTelemetry Tracing...")

    # Define Resource
    resource = Resource.create({
        "service.name": settings.PROJECT_NAME,
        "service.version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    })

    # Tracer Provider
    provider = TracerProvider(resource=resource)
    
    # OTLP Exporter (assuming a collector is available or we use a direct backend)
    # For now, we'll configure it but it might fail if no collector is running
    try:
        otlp_exporter = OTLPSpanExporter(endpoint="http://otel-collector:4317", insecure=True)
        processor = BatchSpanProcessor(otlp_exporter)
        provider.add_span_processor(processor)
    except Exception as e:
        logger.warning(f"Failed to initialize OTLP exporter: {e}. Traces will not be exported.")

    trace.set_tracer_provider(provider)

    # Instrument FastAPI
    FastAPIInstrumentor.instrument_app(app)
    
    logger.info("OpenTelemetry Instrumentation complete.")
