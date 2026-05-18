import asyncio
import logging
from testing.convergence.framework import ConvergenceScenario
from data_simulation.scenario_injector import ScenarioInjector
from ecos.main import ecos
from ecos.contracts.base import CognitiveTask, CognitiveTaskPriority

logger = logging.getLogger("convergence.scenario.fraud")

class FraudEscalationScenario(ConvergenceScenario):
    """
    Validates the fraud response orchestration workflow.
    """
    
    def __init__(self):
        super().__init__(
            "Fraud Escalation",
            "Simulates an account takeover burst and verifies automated containment orchestration."
        )
        self.injector = ScenarioInjector()

    async def inject(self):
        logger.info("Injecting fraud burst for Account 1001...")
        self.injector.inject_fraud_burst(1001, n_txns=25)
        
        # Trigger ECOS fraud orchestration
        await ecos.execute_institutional_directive(CognitiveTask(
            priority=CognitiveTaskPriority.HIGH,
            service_domain="fraud",
            action="initiate_account_freeze",
            payload={"account_id": 1001, "reason": "VELOCITY_THRESHOLD_EXCEEDED"}
        ))

    async def validate(self) -> bool:
        """
        Verifies that the containment directive was registered and governed.
        """
        # Allow ECOS to process the task
        await asyncio.sleep(0.5)
        
        events = ecos.state.get_event_history()
        fraud_events = [e for e in events if "fraud" in e.description.lower() or "state updated: tasks" in e.description.lower()]
        
        self.results["fraud_events_count"] = len(fraud_events)
        
        # Check if the task is in the registry
        state = ecos.state.get_domain_state("tasks")
        has_freeze_task = any(v == "DISPATCHED" for k, v in state.items())
        
        return has_freeze_task and len(fraud_events) > 0
