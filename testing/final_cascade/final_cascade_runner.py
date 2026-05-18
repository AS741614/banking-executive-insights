import asyncio
import logging
import sys

from testing.final_cascade.crisis_injector import InstitutionalCrisisInjector
from testing.final_cascade.validation_framework import ConvergenceValidationFramework

# Configure logging for executive validation run
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger("esoteric_bank.testing.cascade_runner")

async def run_final_cascade():
    logger.info("Starting ESOTERIC BANK Final Institutional Event Cascade...")
    
    injector = InstitutionalCrisisInjector()
    validator = ConvergenceValidationFramework()

    # 1. Inject the Crisis Convergence Scenario
    await injector.execute_full_cascade()
    
    # Let the asynchronous event bus and cognitive engines process the events
    logger.info("Awaiting cognitive event propagation across institutional nodes...")
    await asyncio.sleep(2)

    # 2. Validate Platform Convergence
    print("\n--- INITIATING SYSTEM-WIDE CONVERGENCE VALIDATION ---")
    await validator.validate_fraud_containment()
    await validator.validate_aml_escalation()
    await validator.validate_governance_orchestration()
    await validator.validate_observability_streaming()
    
    # 3. Generate Final Executive Certification Report
    validator.generate_convergence_report()

if __name__ == "__main__":
    asyncio.run(run_final_cascade())
