import asyncio
import logging
import sys

from demo.orchestration.scenario_orchestrator import ScenarioOrchestrator
from demo.scenarios.scenario_registry import get_aml_escalation_scenario, get_fraud_prevention_scenario

# Configure logging for demo visibility
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)

async def run_demo():
    orchestrator = ScenarioOrchestrator()
    
    # 1. Run AML Escalation Demo
    aml_scenario = get_aml_escalation_scenario()
    await orchestrator.execute_scenario(aml_scenario)
    
    print("\n--- Transitioning to next scenario ---\n")
    await asyncio.sleep(2)
    
    # 2. Run Fraud Prevention Demo
    fraud_scenario = get_fraud_prevention_scenario()
    await orchestrator.execute_scenario(fraud_scenario)

if __name__ == "__main__":
    asyncio.run(run_demo())
