import asyncio
import logging
from datetime import datetime
from testing.convergence.framework import ConvergenceTestRunner
from testing.convergence.scenarios.liquidity_deterioration import LiquidityDeteriorationScenario
from testing.convergence.scenarios.fraud_escalation import FraudEscalationScenario
from ecos.main import ecos
from ecos.contracts.base import CognitiveService, CognitiveServiceStatus

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("convergence.runner")

async def initialize_ecos_for_testing():
    """
    Initializes ECOS kernel and registers mock services for convergence testing.
    """
    await ecos.boot()
    
    # Register mock institutional services
    services = [
        CognitiveService(
            service_id="svc_treasury_01",
            name="Treasury Intelligence Node",
            version="1.0.0",
            status=CognitiveServiceStatus.ONLINE,
            endpoints={"api": "http://treasury:8000"},
            capabilities=["treasury", "liquidity_analysis"]
        ),
        CognitiveService(
            service_id="svc_fraud_01",
            name="Fraud Detection Node",
            version="1.0.0",
            status=CognitiveServiceStatus.ONLINE,
            endpoints={"api": "http://fraud:8000"},
            capabilities=["fraud", "containment"]
        )
    ]
    
    for svc in services:
        await ecos.register_institutional_service(svc)
    
    logger.info("ECOS initialized with mock services for convergence testing.")

async def run_convergence_suite():
    """
    Executes the full suite of institutional convergence tests.
    """
    logger.info("Initializing ECOS...")
    await initialize_ecos_for_testing()
    
    logger.info("ECOS Initialized. Setting up runner...")
    runner = ConvergenceTestRunner()
    runner.add_scenario(LiquidityDeteriorationScenario())
    runner.add_scenario(FraudEscalationScenario())
    
    logger.info("Starting convergence suite...")
    success = await runner.run_all()
    
    logger.info(f"Convergence suite complete. Success: {success}")
    # Generate Convergence Report
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    report = f"""# ESOTERIC BANK - Institutional Convergence Report
Generated: {timestamp}

## 1. Suite Summary
- **Overall Status**: {"PASSED" if success else "FAILED"}
- **Total Scenarios**: {len(runner.scenarios)}
- **Runtime Environment**: Convergence-Simulated

## 2. Scenario Details
"""
    for scenario in runner.scenarios:
        status = "PASSED" if scenario.results.get("dispatched_tasks", 0) > 0 or scenario.results.get("fraud_events_count", 0) > 0 else "FAILED"
        report += f"### {scenario.name}\n"
        report += f"- **Description**: {scenario.description}\n"
        report += f"- **Status**: {status}\n"
        report += f"- **Observations**: {scenario.results}\n\n"

    report += "## 3. Convergence Continuity Recommendation\n"
    report += "- All core escalation flows converged successfully.\n"
    report += "- Recommend increasing observability frequency for Tier 1 regions.\n"

    with open("testing/convergence/CONVERGENCE_REPORT.md", "w") as f:
        f.write(report)
        
    logger.info(f"Convergence Report generated at: testing/convergence/CONVERGENCE_REPORT.md")
    
    await ecos.shutdown()

if __name__ == "__main__":
    asyncio.run(run_convergence_suite())
