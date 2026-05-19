import logging
from typing import Dict, Any, List
from ecos.main import ecos
from ecos.contracts.base import CognitiveTask, CognitiveService

logger = logging.getLogger("ecos.api.coordination")

class EnterpriseCoordinationAPI:
    """
    Exposes high-level coordination APIs for institutional services and operators.
    Provides a governance-safe interface to the ECOS Kernel.
    """
    
    @staticmethod
    async def submit_directive(directive_data: Dict[str, Any]) -> str:
        """
        Submits an institutional directive to the OS kernel.
        """
        task = CognitiveTask(**directive_data)
        await ecos.execute_institutional_directive(task)
        return task.task_id

    @staticmethod
    async def get_institutional_awareness() -> Dict[str, Any]:
        """
        Retrieves the current executive-level snapshot of the OS state.
        """
        return await ecos.awareness.get_executive_snapshot()

    @staticmethod
    async def register_node(service_data: Dict[str, Any]):
        """
        Registers a new cognitive node into the enterprise topology.
        """
        service = CognitiveService(**service_data)
        await ecos.register_institutional_service(service)
        return {"status": "REGISTERED", "service_id": service.service_id}

    @staticmethod
    async def get_topology_map() -> List[Dict[str, Any]]:
        """
        Returns the current network map of cognitive services.
        """
        topology = await ecos.topology.get_current_topology()
        return [s.dict() for s in topology.services]
