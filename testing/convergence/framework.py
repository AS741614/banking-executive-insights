import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("convergence.framework")

class ConvergenceScenario(ABC):
    """
    Base class for institutional convergence scenarios.
    Each scenario defines a failure or stress state to validate system response.
    """
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.results: Dict[str, Any] = {}

    @abstractmethod
    async def inject(self):
        """Injects the stress state into the system (data or state)."""
        pass

    @abstractmethod
    async def validate(self) -> bool:
        """Validates that the system correctly detected and responded to the scenario."""
        pass

class ConvergenceTestRunner:
    """
    Orchestrates the execution of multiple convergence scenarios.
    """
    
    def __init__(self):
        self.scenarios: List[ConvergenceScenario] = []

    def add_scenario(self, scenario: ConvergenceScenario):
        self.scenarios.append(scenario)

    async def run_all(self):
        logger.info("--- STARTING INSTITUTIONAL CONVERGENCE TESTING ---")
        overall_success = True
        
        for scenario in self.scenarios:
            logger.info(f"Executing Scenario: {scenario.name}")
            try:
                await scenario.inject()
                success = await scenario.validate()
                if not success:
                    overall_success = False
                    logger.error(f"Scenario FAILED: {scenario.name}")
                else:
                    logger.info(f"Scenario PASSED: {scenario.name}")
            except Exception as e:
                overall_success = False
                logger.error(f"Scenario CRASHED: {scenario.name} | Error: {e}")

        logger.info("--- CONVERGENCE TESTING COMPLETE ---")
        return overall_success
