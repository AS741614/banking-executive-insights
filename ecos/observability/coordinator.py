import logging
import json
from typing import Dict, Any
from ecos.state.registry import InstitutionalStateRegistry
from ecos.contracts.base import OrchestrationEvent

logger = logging.getLogger("ecos.observability.coordinator")

class CognitiveObservabilityCoordination:
    """
    Coordinates cognitive observability by bridging ECOS events with platform monitoring.
    Ensures every orchestration decision is traceable and audit-ready.
    """
    
    def __init__(self, state_registry: InstitutionalStateRegistry):
        self.state = state_registry

    async def export_orchestration_metrics(self):
        """
        Exports current orchestration events and metrics to institutional logs.
        """
        events = await self.state.get_event_history(limit=50)
        logger.info(f"Exporting {len(events)} orchestration events to institutional audit log.")
        
        for event in events:
            # Structured logging for ELK/Splunk integration
            log_entry = {
                "source": "ECOS",
                "event_id": event.event_id,
                "timestamp": event.timestamp.isoformat(),
                "type": event.event_type,
                "severity": event.severity,
                "description": event.description,
                "context": event.metadata
            }
            # In production, this would go to a specialized stream
            # For now, we use structured standard output
            logger.info(f"AUDIT_LOG: {json.dumps(log_entry)}")

    async def get_system_telemetry(self) -> Dict[str, Any]:
        """
        Aggregates system-level telemetry for observability dashboards.
        """
        system_state = await self.state.get_domain_state("system")
        return {
            "kernel_status": system_state.get("kernel_status", "UNKNOWN"),
            "event_velocity": len(await self.state.get_event_history(limit=100)),
            "last_sync": system_state.get("active_topology_version", 0)
        }
