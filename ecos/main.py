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
from ecos.core.event_bus import event_bus
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
        
        # Setup Reactive Subscriptions
        await self.setup_subscriptions()
        
        # Start core components
        await self.runtime.start()
        await self.scheduler.start()
        await self.sync.start()
        
        # Initialize Runtime Health Monitoring
        asyncio.create_task(monitor.monitor_institutional_stack())
        
        logger.info("ECOS Kernel Boot Sequence Complete. System Operational.")
        await self.state.set_state(domain="system", key="kernel_status", value="READY")

    async def setup_subscriptions(self):
        """
        Sets up reactive event subscriptions between ECOS layers.
        """
        logger.info("Establishing institutional event propagation channels...")
        # Governance reacting to state updates
        await event_bus.subscribe("STATE_UPDATE", self.governance.handle_state_update)
        
        # Bridge Cognitive Event Bus to ECOS State
        from ai.events.engines.event_bus import event_bus as cognitive_event_bus
        for category in ["COGNITION", "GOVERNANCE", "COMPLIANCE", "OPERATIONAL", "ADAPTIVE"]:
            cognitive_event_bus.subscribe(category, self.handle_cognitive_event)
            
        logger.info("Event propagation channels ESTABLISHED.")

    async def handle_cognitive_event(self, event):
        """
        Handles events from the cognitive bus and reflects them in the ECOS state.
        """
        await self.state.set_state(
            domain="events",
            key=event.event_id,
            value=event.dict(),
            metadata={"category": event.category, "severity": event.severity}
        )
        
        # Adaptive Metric Propagation
        if event.action == "LIQUIDITY_DETERIORATION":
            await self.state.set_state(domain="risk", key="liquidity_risk", value=event.payload.get("liquidity_coverage_ratio", 0.8))
        elif event.action == "GOVERNANCE_DRIFT_DETECTED":
            await self.state.set_state(domain="governance", key="drift_index", value=event.payload.get("variance", 0.0))
        elif event.action == "ANOMALY_DETECTED" or event.action == "DEVICE_RISK_IDENTIFIED":
            current = await self.state.get_state("risk", "anomalies_detected")
            count = (current.value if current else 0) + 1
            await self.state.set_state(domain="risk", key="anomalies_detected", value=count)

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
        if await self.governance.validate_task(task):
            await self.runtime.submit_task(task)
        else:
            logger.warning(f"Institutional Directive REJECTED by Governance: {task.task_id}")

    async def register_institutional_service(self, service: CognitiveService):
        """
        Connects an institutional cognitive service to the ECOS.
        """
        await self.runtime.register_service(service)

# Singleton instance for the platform
ecos = EnterpriseCognitionOS()
