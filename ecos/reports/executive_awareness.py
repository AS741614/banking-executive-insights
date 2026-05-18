import logging
from typing import Dict, Any, List
from ecos.state.registry import InstitutionalStateRegistry
from ecos.contracts.base import CognitiveServiceStatus

logger = logging.getLogger("ecos.executive.awareness")

class ExecutiveStateAwareness:
    """
    Provides a high-level, executive-focused view of the ECOS runtime state.
    Aggregates institutional intelligence for decision-making.
    """
    
    def __init__(self, state_registry: InstitutionalStateRegistry):
        self.state = state_registry

    def get_executive_snapshot(self) -> Dict[str, Any]:
        """
        Generates a summary of the enterprise cognitive state.
        """
        topology = self.state.get_domain_state("topology")
        system_status = self.state.get_state("system", "runtime_status")
        
        # Calculate health metrics
        total_services = len(topology)
        online_services = sum(1 for s in topology.values() if s.get("status") == CognitiveServiceStatus.ONLINE)
        
        # Aggregate active tasks
        tasks = self.state.get_domain_state("tasks")
        queued_tasks = sum(1 for status in tasks.values() if status == "QUEUED")
        dispatched_tasks = sum(1 for status in tasks.values() if status == "DISPATCHED")
        
        return {
            "institutional_health": {
                "system_status": system_status.value if system_status else "UNKNOWN",
                "cognitive_capacity": f"{online_services}/{total_services} Nodes Online",
                "orchestration_efficiency": "OPTIMAL" if queued_tasks < 10 else "CONGESTED"
            },
            "active_intelligence_streams": {
                "queued_directives": queued_tasks,
                "in_flight_tasks": dispatched_tasks
            },
            "governance_posture": "SECURE",
            "last_synchronized": datetime.utcnow().isoformat()
        }

from datetime import datetime
