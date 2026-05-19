from fastapi import APIRouter, Request
from datetime import datetime
from typing import Any, Dict

from app.schemas.common import EnterpriseResponse, EnterpriseMetadata

router = APIRouter()

def create_enterprise_response(request: Request, domain: str, data: Dict[str, Any]) -> EnterpriseResponse:
    trace_id = request.headers.get("X-Enterprise-Trace-Id")
    return EnterpriseResponse(
        meta=EnterpriseMetadata(
            status="success",
            timestamp=datetime.utcnow().isoformat(),
            trace_id=trace_id,
            version="1.0"
        ),
        data={"domain": domain, **data}
    )

from app.services.warehouse_service import WarehouseService
from ai.observability.services.telemetry_aggregator import ExecutiveTelemetryAggregator

telemetry_aggregator = ExecutiveTelemetryAggregator()

@router.get("/executive/intelligence")
async def executive_intelligence(request: Request) -> Any:
    health = await telemetry_aggregator.get_institutional_health_snapshot()
    return create_enterprise_response(request, "Executive Intelligence", health)

@router.get("/risk/intelligence")
async def risk_intelligence(request: Request) -> Any:
    risk = WarehouseService.get_risk_metrics()
    # Bind to live anomaly propagation from ECOS state
    live_risk = await ecos.state.get_domain_state("risk")
    return create_enterprise_response(request, "Risk Intelligence", {**risk, "live_risk_state": live_risk})

@router.get("/governance/cognition")
async def governance_cognition(request: Request) -> Any:
    # Bind to governance runtime state
    status = await ecos.state.get_domain_state("governance")
    return create_enterprise_response(request, "Governance", status)

@router.get("/forecast/intelligence")
async def forecast_intelligence(request: Request) -> Any:
    forecast = WarehouseService.get_forecast_metrics()
    return create_enterprise_response(request, "Forecasting", forecast)

from ai.events.engines.event_streamer import event_streamer

@router.get("/events/intelligence")
async def events_intelligence(request: Request, trigger_cascade: bool = False) -> Any:
    # Trigger adaptive cascade if requested (for convergence validation)
    if trigger_cascade:
        from testing.final_cascade.crisis_injector import InstitutionalCrisisInjector
        injector = InstitutionalCrisisInjector()
        await injector.execute_full_cascade()
        
    # Bind to live event bus state from ECOS state registry (Cognitive Events)
    events = await ecos.state.get_domain_state("events")
    critical = [e for e in events.values() if e.get("severity") == "CRITICAL"]
    
    return create_enterprise_response(request, "Events", {
        "active_events": len(events),
        "critical_events": len(critical),
        "total_event_throughput": len(events)
    })

from ecos.main import ecos

@router.get("/agents/distributed")
async def distributed_agents(request: Request) -> Any:
    topology = await ecos.state.get_domain_state("topology")
    return create_enterprise_response(request, "Agents", {
        "active_agents": len(topology),
        "agents": list(topology.keys()),
        "system_state": "SYNCHRONIZED" if len(topology) > 0 else "BOOTING"
    })

@router.get("/memory/snapshots")
async def memory_snapshots(request: Request) -> Any:
    memory_state = await ecos.state.get_domain_state("memory")
    latest = memory_state.get("latest_snapshot", "no_snapshot_available")
    return create_enterprise_response(request, "Memory", {
        "latest_snapshot": latest,
        "active_keys": len(memory_state),
        "persistence": "READY"
    })