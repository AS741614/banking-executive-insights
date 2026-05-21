import logging
import sys
import os

# Ensure the root directory is in sys.path for absolute imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from ai.tableau.runtime.config import TableauConfig
from ai.tableau.orchestrator.kpi_orchestrator import KPIOrchestrator
from ai.tableau.orchestrator.sync_manager import TableauSyncManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("tableau.automation")

def run_automation():
    logger.info("Starting ESOTERIC BANK Tableau Automation Cycle")
    
    config = TableauConfig()
    
    # 1. KPI Intelligence Orchestration
    logger.info("Phase 1: KPI Intelligence Orchestration")
    kpi_orchestrator = KPIOrchestrator(config)
    kpi_values = kpi_orchestrator.synchronize_kpis()
    
    # 2. Tableau Synchronization and Observability
    logger.info("Phase 2: Tableau Synchronization & Observability")
    sync_manager = TableauSyncManager(config)
    sync_manager.perform_full_sync()
    
    logger.info("Tableau Automation Cycle Completed Successfully")

if __name__ == "__main__":
    try:
        run_automation()
    except Exception as e:
        logger.error(f"Tableau Automation Cycle Failed: {e}")
        sys.exit(1)
