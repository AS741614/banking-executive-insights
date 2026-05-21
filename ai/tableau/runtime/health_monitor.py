import logging
from datetime import datetime, timedelta
from .base_client import TableauBaseClient, TSC

logger = logging.getLogger(__name__)

class HealthMonitor(TableauBaseClient):
    """
    Monitors the health of Tableau refreshes and server connectivity.
    """

    def check_server_health(self):
        """Basic connectivity and authentication check."""
        try:
            with self:
                info = self.server.server_info
                logger.info(f"Connected to Tableau Server version: {info.product_version}")
                return True
        except Exception as e:
            logger.error(f"Server health check failed: {e}")
            return False

    def get_recent_failed_jobs(self, hours: int = 24):
        """Retrieves background jobs that failed in the last N hours."""
        with self:
            req_option = TSC.RequestOptions()
            # Note: TSC filtering for jobs might be limited depending on version
            all_jobs, pagination_item = self.server.jobs.get(req_option)
            
            threshold = datetime.utcnow() - timedelta(hours=hours)
            failed_jobs = []
            
            for job in all_jobs:
                # job.created_at might be available depending on version
                if job.finish_code == '1':
                    failed_jobs.append({
                        "id": job.id,
                        "type": job.type,
                        "notes": job.notes,
                        "finish_code": job.finish_code
                    })
            
            logger.info(f"Found {len(failed_jobs)} failed jobs in the last {hours} hours.")
            return failed_jobs

    def validate_datasources(self, project_id: str):
        """Validates that all datasources in a project are reachable."""
        with self:
            req_option = TSC.RequestOptions()
            req_option.filter.add(TSC.Filter(TSC.Filter.Operator.Equals, TSC.Filter.Field.ProjectId, project_id))
            all_datasources, _ = self.server.datasources.get(req_option)
            
            report = []
            for ds in all_datasources:
                # Basic check: can we get metadata?
                try:
                    self.server.datasources.populate_connections(ds)
                    report.append({"name": ds.name, "status": "OK"})
                except Exception as e:
                    report.append({"name": ds.name, "status": "ERROR", "message": str(e)})
            
            return report
