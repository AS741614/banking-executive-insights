import json
import asyncio
import logging
from fastapi import APIRouter, Request, status
from fastapi.responses import StreamingResponse
from datetime import datetime
from typing import Any, Dict

from app.schemas.common import EnterpriseResponse, EnterpriseMetadata
from app.services.platform_monitor import PlatformMonitor
from ai.events.engines.event_streamer import event_streamer
from ai.observability.services.telemetry_aggregator import ExecutiveTelemetryAggregator

logger = logging.getLogger("esoteric_platform.api.observability")
router = APIRouter()
aggregator = ExecutiveTelemetryAggregator()

@router.get("/health", response_model=EnterpriseResponse[Dict[str, Any]])
async def health_check(request: Request) -> Any:
    """Liveness probe."""
    trace_id = request.headers.get("X-Enterprise-Trace-Id")
    return EnterpriseResponse(
        meta=EnterpriseMetadata(status="success", timestamp=datetime.utcnow().isoformat(), trace_id=trace_id),
        data={"status": "online", "subsystem": "FastAPI Core"}
    )

@router.get("/ready", response_model=EnterpriseResponse[Dict[str, Any]])
async def readiness_check(request: Request) -> Any:
    """Readiness probe."""
    trace_id = request.headers.get("X-Enterprise-Trace-Id")
    return EnterpriseResponse(
        meta=EnterpriseMetadata(status="success", timestamp=datetime.utcnow().isoformat(), trace_id=trace_id),
        data={"status": "ready", "subsystem": "FastAPI Core"}
    )

@router.get("/status", response_model=EnterpriseResponse[Dict[str, Any]])
async def platform_status(request: Request) -> Any:
    """Institutional health snapshot."""
    trace_id = request.headers.get("X-Enterprise-Trace-Id")
    status_data = await aggregator.get_institutional_health_snapshot()
    return EnterpriseResponse(
        meta=EnterpriseMetadata(status="success", timestamp=datetime.utcnow().isoformat(), trace_id=trace_id),
        data=status_data
    )

@router.get("/stream")
async def event_stream(request: Request):
    """
    Live Cognitive Event Stream (Server-Sent Events).
    Provides real-time visibility into institutional activities.
    """
    trace_id = request.headers.get("X-Enterprise-Trace-Id", "unknown")

    async def event_generator():
        logger.info(f"[SSE_CONNECTED] Client connected to event stream. Trace: {trace_id}")
        queue = event_streamer.subscribe()
        try:
            while True:
                # Check for disconnect at the start of each iteration
                if await request.is_disconnected():
                    logger.info(f"[SSE_CLIENT_DISCONNECTED] Client disconnected detected for trace: {trace_id}")
                    break
                
                try:
                    # Use asyncio.wait_for to allow checking for disconnects and sending heartbeats
                    # Heartbeat interval: 15 seconds as per institutional requirements
                    event = await asyncio.wait_for(queue.get(), timeout=15.0)
                    yield f"data: {event.model_dump_json()}\n\n"
                except asyncio.TimeoutError:
                    # Send a heartbeat (keepalive comment) to maintain connection
                    logger.debug(f"[SSE_HEARTBEAT_SENT] Sending keepalive to trace: {trace_id}")
                    yield ": keepalive\n\n"
                except Exception as e:
                    logger.error(f"[SSE_INTERNAL_ERROR] Error in generator for trace {trace_id}: {str(e)}")
                    # Don't break here, attempt to continue unless it's a fatal error
                    continue
        except asyncio.CancelledError:
            logger.info(f"[SSE_GENERATOR_TERMINATED] Stream cancelled for trace: {trace_id}")
            raise
        except Exception as e:
            logger.error(f"[SSE_EXCEPTION] Fatal generator error for trace: {trace_id} | Error: {str(e)}")
        finally:
            logger.info(f"[SSE_CLEANUP] Unsubscribing trace: {trace_id}")
            event_streamer.unsubscribe(queue)

    return StreamingResponse(
        event_generator(), 
        media_type="text/event-stream",
        headers={
            "Content-Type": "text/event-stream",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable buffering for Nginx
        }
    )

@router.get("/history", response_model=EnterpriseResponse[Dict[str, Any]])
async def event_history(request: Request) -> Any:
    """Retrieves recent institutional event history."""
    trace_id = request.headers.get("X-Enterprise-Trace-Id")
    history = event_streamer.get_recent_history()
    return EnterpriseResponse(
        meta=EnterpriseMetadata(status="success", timestamp=datetime.utcnow().isoformat(), trace_id=trace_id),
        data={"events": [e.model_dump() for e in history]}
    )
