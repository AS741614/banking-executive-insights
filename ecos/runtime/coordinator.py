import logging
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
from ecos.contracts.base import (
    CognitiveTask, 
    CognitiveTaskPriority, 
    CognitiveService, 
    CognitiveServiceStatus,
    OrchestrationEvent,
    CognitiveOrigin
)
from ecos.state.registry import InstitutionalStateRegistry

logger = logging.getLogger("ecos.runtime.coordinator")

class CognitiveRuntimeCoordinator:
    """
    Core orchestration engine for the ESOTERIC Cognitive OS.
    Coordinates distributed cognition tasks and manages service lifecycles.
    """
    
    def __init__(self, state_registry: InstitutionalStateRegistry):
        self.state = state_registry
        self._services: Dict[str, CognitiveService] = {}
        self._task_queue: asyncio.PriorityQueue = asyncio.PriorityQueue()
        self._active_tasks: Dict[str, CognitiveTask] = {}
        self._is_running = False
        self._service_registered_event = asyncio.Event()

    async def register_service(self, service: CognitiveService):
        """
        Registers a new cognitive service into the ECOS topology.
        """
        self._services[service.service_id] = service
        await self.state.set_state(
            domain="topology",
            key=service.service_id,
            value=service.dict(),
            metadata={"type": "service_registration"}
        )
        logger.info(f"Service registered: {service.name} ({service.service_id})")
        
        # Notify the processing loop that a new service is available
        self._service_registered_event.set()
        self._service_registered_event.clear()

    async def submit_task(self, task: CognitiveTask):
        """
        Submits a task to the cognitive runtime.
        """
        # Priority mapping for asyncio.PriorityQueue (lower value = higher priority)
        priority_map = {
            CognitiveTaskPriority.CRITICAL: 0,
            CognitiveTaskPriority.HIGH: 1,
            CognitiveTaskPriority.NORMAL: 2,
            CognitiveTaskPriority.LOW: 3
        }
        
        priority_val = priority_map.get(task.priority, 2)
        await self._task_queue.put((priority_val, datetime.utcnow(), task))
        
        logger.info(f"Task submitted: {task.task_id} [Priority: {task.priority.name}] [Origin: {task.origin.name}]")
        await self.state.set_state(
            domain="tasks",
            key=task.task_id,
            value="QUEUED",
            origin=task.origin,
            metadata={
                "priority": task.priority.name, 
                "domain": task.service_domain,
                "correlation_id": task.correlation_id
            }
        )

    async def _process_tasks(self):
        """
        Internal loop to dispatch tasks to appropriate services.
        """
        while self._is_running:
            try:
                priority, ts, task = await self._task_queue.get()
                
                while self._is_running:
                    # Find available service for the domain
                    target_service = self._find_service_for_domain(task.service_domain)
                    
                    if target_service:
                        await self._dispatch_task(task, target_service)
                        break
                    else:
                        logger.warning(f"No active service found for domain: {task.service_domain}. Waiting for service registration...")
                        # Wait for a new service to be registered before trying again
                        try:
                            # Operationalized: Wait for event instead of sleep(1) polling
                            await asyncio.wait_for(self._service_registered_event.wait(), timeout=30.0)
                        except asyncio.TimeoutError:
                            logger.info(f"Timeout waiting for service for domain {task.service_domain}. Re-queueing task.")
                            await self._task_queue.put((priority, ts, task))
                            break
                
                self._task_queue.task_done()
            except Exception as e:
                logger.error(f"Error in task processing loop: {e}")
                await asyncio.sleep(1)

    def _find_service_for_domain(self, domain: str) -> Optional[CognitiveService]:
        """
        Selects a service that supports the requested domain and is ONLINE.
        """
        for service in self._services.values():
            if domain in service.capabilities and service.status == CognitiveServiceStatus.ONLINE:
                return service
        return None

    async def _dispatch_task(self, task: CognitiveTask, service: CognitiveService):
        """
        Dispatches a task to a specific service.
        """
        logger.info(f"Dispatching task {task.task_id} to service {service.name}")
        self._active_tasks[task.task_id] = task
        await self.state.set_state(
            domain="tasks", 
            key=task.task_id, 
            value="DISPATCHED", 
            origin=task.origin,
            metadata={
                "service": service.name,
                "correlation_id": task.correlation_id
            }
        )
        
        # Operationalized: No more asyncio.sleep(0.1) placeholder.
        # The state update already published a STATE_UPDATE event which triggers downstream orchestration.

    async def start(self):
        """
        Starts the ECOS runtime coordinator.
        """
        logger.info("Starting ESOTERIC Cognitive OS Runtime Coordinator...")
        self._is_running = True
        asyncio.create_task(self._process_tasks())
        
        await self.state.set_state(
            domain="system",
            key="runtime_status",
            value="OPERATIONAL",
            metadata={"startup_time": datetime.utcnow().isoformat()}
        )

    async def stop(self):
        """
        Gracefully shuts down the coordinator.
        """
        logger.info("Shutting down ECOS Runtime Coordinator...")
        self._is_running = False
        # Wait for queue to empty or timeout
        # self._task_queue.join()
