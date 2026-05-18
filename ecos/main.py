import logging
import asyncio
from typing import Optional
from ecos.state.registry import InstitutionalStateRegistry
from ecos.runtime.coordinator import CognitiveRuntimeCoordinator
from ecos.governance.continuity import GovernanceContinuityLayer
from ecos.scheduler.distributed import DistributedCognitionScheduler
from ecos.topology.manager import CognitiveTopologyManager
from ecos.runtime.sync import InstitutionalRuntimeSynchronization
from ecos.reports.executive_awareness import ExecutiveStateAwareness
from ecos.observability.coordinator import CognitiveObservabilityCoordination
from ecos.contracts.base import CognitiveTask, CognitiveService
from runtime.performance import optimizer
from runtime.health.monitor import monitor

logger = logging.getLogger("ecos.main")

class EnterpriseCognitionOS:
    """
    Main entry point for the ESOTERIC Enterprise Cognitive Operating System (ECOS).
    Orchestrates the runtime, state, and governance of distributed cognition.
    """
    
    def __init__(self):
        logger.info("Initializing ESOTERIC Enterprise Cognitive Operating System...")
        
        # 1. Institutional State Registry (Foundation)
        self.state = InstitutionalStateRegistry()
        
        # 2. Cognitive Runtime Coordinator (Engine)
        self.runtime = CognitiveRuntimeCoordinator(self.state)
        
        # 3. Governance Continuity Layer (Policy)
        self.governance = GovernanceContinuityLayer(self.state)
        
        # 4. Distributed Cognition Scheduler (Temporal)
        self.scheduler = DistributedCognitionScheduler(self.runtime)
        
        # 5. Cognitive Topology Manager (Network)
        self.topology = CognitiveTopologyManager(self.state)
        
        # 6. Institutional Runtime Synchronization (Sync)
        self.sync = InstitutionalRuntimeSynchronization(self.state, self.topology)
        
        # 7. Executive State Awareness (Reporting)
        self.awareness = ExecutiveStateAwareness(self.state)
        
        # 8. Cognitive Observability Coordination (Audit)
        self.observability = CognitiveObservabilityCoordination(self.state)

    async def boot(self):
        """
        Boots the cognitive operating system.
        """
        logger.info("Booting ECOS Kernel...")
        
        # Optimize Event Loop for Production
        optimizer.optimize_event_loop()
        
        # Start core components
        await self.runtime.start()
        await self.scheduler.start()
        await self.sync.start()
        
        # Initialize Runtime Health Monitoring
        asyncio.create_task(monitor.monitor_institutional_stack())
        
        logger.info("ECOS Kernel Boot Sequence Complete. System Operational.")
        self.state.set_state(domain="system", key="kernel_status", value="READY")

    async def shutdown(self):
        """
        Gracefully shuts down the operating system.
        """
        logger.info("Initiating ECOS Shutdown Sequence...")
        await self.sync.stop()
        await self.scheduler.stop()
        await self.runtime.stop()
        logger.info("ECOS Shutdown Complete.")

    async def execute_institutional_directive(self, task: CognitiveTask):
        """
        Submits a directive to the ECOS for governed execution.
        """
        if self.governance.validate_task(task):
            await self.runtime.submit_task(task)
        else:
            logger.warning(f"Institutional Directive REJECTED by Governance: {task.task_id}")

    def register_institutional_service(self, service: CognitiveService):
        """
        Connects an institutional cognitive service to the ECOS.
        """
        self.runtime.register_service(service)

# Singleton instance for the platform
ecos = EnterpriseCognitionOS()
