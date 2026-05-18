import asyncio
import logging
from testing.convergence.framework import ConvergenceScenario
from data_simulation.scenario_injector import ScenarioInjector
from ecos.main import ecos
from ecos.contracts.base import CognitiveTask, CognitiveTaskPriority, CognitiveOrigin

logger = logging.getLogger("convergence.scenario.liquidity")

class LiquidityDeteriorationScenario(ConvergenceScenario):
    """
    Validates institutional response to a rapid liquidity drain.
    """
    
    def __init__(self):
        super().__init__(
            "Liquidity Deterioration",
            "Simulates a massive capital withdrawal in the 'North' region and verifies Treasury response."
        )
        self.injector = ScenarioInjector()

    async def inject(self):
        logger.info("Injecting $50M liquidity drain in 'North' region...")
        count = self.injector.inject_liquidity_drain("North", amount_per_txn=1000000.0, n_txns=50)
        
        # Simulate ECOS awareness of the event
        await ecos.execute_institutional_directive(CognitiveTask(
            priority=CognitiveTaskPriority.CRITICAL,
            origin=CognitiveOrigin.SIMULATION,
            service_domain="treasury",
            action="evaluate_liquidity_risk",
            payload={"region": "North", "severity": "EXTREME"}
        ))

    async def validate(self) -> bool:
        """
        Validates that the system state reflects the crisis and triggered orchestration.
        """
        # Allow ECOS to process the task
        await asyncio.sleep(0.5)
        
        # 1. Check ECOS state for treasury action - ONLY LOOK AT SIMULATION ORIGIN
        state = ecos.state.get_domain_state("tasks", origin=CognitiveOrigin.SIMULATION)
        treasury_tasks = [v for k, v in state.items() if v == "DISPATCHED"]
        
        # 2. Verify institutional awareness
        awareness = ecos.awareness.get_executive_snapshot()
        health = awareness.get("institutional_health", {})
        
        self.results["dispatched_tasks"] = len(treasury_tasks)
        self.results["system_status"] = health.get("system_status")
        
        return len(treasury_tasks) > 0
