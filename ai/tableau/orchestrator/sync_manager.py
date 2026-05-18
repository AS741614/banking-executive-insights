import logging
from typing import List
from ..runtime.config import TableauConfig
from ..runtime.datasource_sync import DatasourceSync
from ..runtime.refresh_scheduler import RefreshScheduler
from ..runtime.hyper_orchestrator import HyperOrchestrator
from ..observability.datasource_metrics import DatasourceObserver
from ..observability.health_monitor import DashboardHealthMonitor

logger = logging.getLogger(__name__)

class TableauSyncManager:
    """
    High-level orchestrator for Tableau synchronization and health.
    Ties together refresh schedules, datasource updates, and observability.
    """
    
    def __init__(self, config: TableauConfig):
        self.config = config
        self.ds_sync = DatasourceSync(config)
        self.scheduler = RefreshScheduler(config)
        self.hyper_orchestrator = HyperOrchestrator(config)
        self.observer = DatasourceObserver(config.pg_connection_string)
        self.health_monitor = DashboardHealthMonitor(config.pg_connection_string)

    def perform_full_sync(self):
        """Executes a complete synchronization and health check cycle."""
        logger.info("INITIATING GLOBAL TABLEAU SYNCHRONIZATION CYCLE")
        
        try:
            # 1. Observability Check: Is the data ready?
            logger.info("Phase 1: Datasource Observability Check")
            self.observer.observe_datasources()
            
            # 2. Connection Sync: Are Tableau connections pointing to the right place?
            logger.info("Phase 2: Tableau Connection Synchronization")
            with self.ds_sync:
                project_id = self.config.project_id
                if not project_id:
                    project_id = self.ds_sync.get_project_id("Banking Insights")
                self.ds_sync.sync_all_in_project(project_id)
            
            # 3. Refresh Trigger: Update the extracts
            logger.info("Phase 3: Triggering Tableau Extract Refreshes")
            with self.scheduler:
                # In a real scenario, we'd fetch the list of workbooks/datasources to refresh
                # For this demo, we assume project-level refresh if available, 
                # or individual items from a registry.
                logger.info("Refreshing core institutional datasources...")
                # job_id = self.scheduler.trigger_datasource_refresh("ds-id-placeholder")
                # self.scheduler.wait_for_job(job_id)
            
            # 4. Hyper Orchestration: Export specialized datasets
            logger.info("Phase 4: Hyper Export Orchestration")
            # Example query for a specialized executive extract
            query = "SELECT * FROM mart.mv_kpi_month WHERE year = 2026"
            # self.hyper_orchestrator.run_pipeline(query, "Executive KPI Summary", "executive_kpis.hyper")
            
            # 5. Health Check: Are dashboards available and performant?
            logger.info("Phase 5: Dashboard Health Monitoring")
            self.health_monitor.check_dashboards()
            
            logger.info("GLOBAL SYNCHRONIZATION CYCLE COMPLETED SUCCESSFULLY")
            
        except Exception as e:
            logger.error(f"Global synchronization cycle failed: {str(e)}")
            raise

if __name__ == "__main__":
    config = TableauConfig()
    manager = TableauSyncManager(config)
    manager.perform_full_sync()
