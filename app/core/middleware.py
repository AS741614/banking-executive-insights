import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger("esoteric_platform.middleware")

class EnterpriseObservabilityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Enterprise Tracking ID generation could go here
        trace_id = request.headers.get("X-Enterprise-Trace-Id", "trace-generated-id")
        
        logger.info(f"Incoming Request: {request.method} {request.url.path} [Trace: {trace_id}]")
        
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            response.headers["X-Enterprise-Trace-Id"] = trace_id
            
            logger.info(f"Request Completed: {request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.4f}s")
            return response
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(f"Request Failed: {request.method} {request.url.path} - Time: {process_time:.4f}s - Error: {str(e)}")
            raise