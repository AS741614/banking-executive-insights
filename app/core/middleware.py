import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging
from opentelemetry import trace

logger = logging.getLogger("esoteric_platform.middleware")
tracer = trace.get_tracer(__name__)

class EnterpriseObservabilityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Get the current span created by OTel FastAPI instrumentation
        current_span = trace.get_current_span()

        # Enterprise Tracking ID generation could go here
        trace_id = request.headers.get("X-Enterprise-Trace-Id")
        if not trace_id:
            # Fallback to OTel trace_id if available
            span_context = current_span.get_span_context()
            if span_context.is_valid:
                trace_id = format(span_context.trace_id, '032x')
            else:
                trace_id = "trace-generated-id"

        current_span.set_attribute("enterprise.trace_id", trace_id)
        current_span.set_attribute("http.method", request.method)
        current_span.set_attribute("http.url", str(request.url))
        
        # Institutional Regional Attribution
        # In a real system, this would be derived from the auth token or request headers
        region = request.headers.get("X-Institutional-Region", "Global")
        segment = request.headers.get("X-Institutional-Segment", "General")
        current_span.set_attribute("institutional.region", region)
        current_span.set_attribute("institutional.segment", segment)

        logger.info(f"Incoming Request: {request.method} {request.url.path} [Trace: {trace_id}] [Region: {region}]")

        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            response.headers["X-Enterprise-Trace-Id"] = trace_id

            current_span.set_attribute("http.status_code", response.status_code)
            current_span.set_attribute("process_time_s", process_time)

            logger.info(f"Request Completed: {request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.4f}s")
            return response
        except Exception as e:
            process_time = time.time() - start_time
            current_span.record_exception(e)
            current_span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))

            logger.error(f"Request Failed: {request.method} {request.url.path} - Time: {process_time:.4f}s - Error: {str(e)}")
            raise