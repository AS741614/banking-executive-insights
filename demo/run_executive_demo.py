import asyncio
import logging
import sys
from demo.orchestration.scenario_orchestrator import ScenarioOrchestrator
from demo.scenarios.scenario_registry import (
    get_aml_escalation_scenario, 
    get_fraud_prevention_scenario,
    get_governance_escalation_scenario,
    get_liquidity_crisis_scenario
)

# Configure high-visibility logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(name)s] - %(levelname)s - %(message)s",
    stream=sys.stdout
)

async def run_full_executive_suite():
    """
    Executes the full suite of institutional demo scenarios.
    """
    orchestrator = ScenarioOrchestrator()
    scenarios = [
        get_aml_escalation_scenario(),
        get_fraud_prevention_scenario(),
        get_governance_escalation_scenario(),
        get_liquidity_crisis_scenario()
    ]
    
    print("\n" + "="*60)
    print("ESOTERIC BANK - INSTITUTIONAL EXECUTIVE DEMO SUITE")
    print("="*60 + "\n")

    for scenario in scenarios:
        print(f"\n>>> INITIATING: {scenario.name}")
        print(f"Narrative: {scenario.executive_narrative}\n")
        await orchestrator.execute_scenario(scenario)
        print(f"\n>>> COMPLETED: {scenario.name}")
        print("-" * 40)
        await asyncio.sleep(2)

    print("\n" + "="*60)
    print("EXECUTIVE DEMO SUITE EXECUTION COMPLETE")
    print(f"Total Events Logged: {len(orchestrator.get_replay_data())}")
    print("="*60 + "\n")

if __name__ == "__main__":
    asyncio.run(run_full_executive_suite())
