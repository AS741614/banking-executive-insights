import json
import asyncio
from fastapi import APIRouter, Request, status
from fastapi.responses import StreamingResponse
from datetime import datetime
from typing import Any, Dict

from app.schemas.common import EnterpriseResponse, EnterpriseMetadata
from app.services.platform_monitor import PlatformMonitor
from ai.events.engines.event_streamer import event_streamer
from ai.observability.services.telemetry_aggregator import ExecutiveTelemetryAggregator

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
    async def event_generator():
        queue = event_streamer.subscribe()
        try:
            while True:
                # If client disconnects, stop streaming
                if await request.is_disconnected():
                    break
                
                event = await queue.get()
                yield f"data: {event.model_dump_json()}\n\n"
        finally:
            event_streamer.unsubscribe(queue)

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@router.get("/history", response_model=EnterpriseResponse[Dict[str, Any]])
async def event_history(request: Request) -> Any:
    """Retrieves recent institutional event history."""
    trace_id = request.headers.get("X-Enterprise-Trace-Id")
    history = event_streamer.get_recent_history()
    return EnterpriseResponse(
        meta=EnterpriseMetadata(status="success", timestamp=datetime.utcnow().isoformat(), trace_id=trace_id),
        data={"events": [e.model_dump() for e in history]}
    )
