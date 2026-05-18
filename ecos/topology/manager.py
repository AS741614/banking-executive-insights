import logging
from typing import Dict, List, Optional
from datetime import datetime
from ecos.contracts.base import CognitiveService, CognitiveServiceStatus, CognitiveTopology
from ecos.state.registry import InstitutionalStateRegistry

logger = logging.getLogger("ecos.topology.manager")

class CognitiveTopologyManager:
    """
    Manages the mapping and synchronization of the enterprise cognitive topology.
    Provides institutional awareness of distributed service nodes.
    """
    
    def __init__(self, state_registry: InstitutionalStateRegistry):
        self.state = state_registry
        self._topology_version = 0

    def update_service_heartbeat(self, service_id: str, status: CognitiveServiceStatus = CognitiveServiceStatus.ONLINE):
        """
        Updates the heartbeat and status of a cognitive service.
        """
        service_data = self.state.get_state("topology", service_id)
        if service_data:
            service_dict = service_data.value
            service_dict["status"] = status
            service_dict["last_heartbeat"] = datetime.utcnow().isoformat()
            
            self.state.set_state(
                domain="topology",
                key=service_id,
                value=service_dict,
                metadata={"type": "heartbeat_update"}
            )
            logger.debug(f"Heartbeat updated for service: {service_id}")
        else:
            logger.warning(f"Heartbeat received for unknown service: {service_id}")

    def get_current_topology(self) -> CognitiveTopology:
        """
        Generates the current view of the enterprise cognitive topology.
        """
        service_states = self.state.get_domain_state("topology")
        services = []
        for s_dict in service_states.values():
            services.append(CognitiveService(**s_dict))
            
        self._topology_version += 1
        return CognitiveTopology(
            version=self._topology_version,
            services=services
        )

    def get_service_by_capability(self, capability: str) -> List[CognitiveService]:
        """
        Returns all services that support a specific capability.
        """
        topology = self.get_current_topology()
        return [s for s in topology.services if capability in s.capabilities and s.status == CognitiveServiceStatus.ONLINE]
