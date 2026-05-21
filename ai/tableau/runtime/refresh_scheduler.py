import logging
import time
from .base_client import TableauBaseClient, TSC
from .config import TableauConfig

logger = logging.getLogger(__name__)

class RefreshScheduler(TableauBaseClient):
    """
    Orchestrates Tableau Dashboard and Datasource refreshes.
    """
    
    def trigger_workbook_refresh(self, workbook_id: str):
        """Triggers an extract refresh for a specific workbook."""
        logger.info(f"Triggering refresh for workbook: {workbook_id}")
        workbook = self.server.workbooks.get_by_id(workbook_id)
        job = self.server.workbooks.refresh(workbook)
        logger.info(f"Refresh job created: {job.id}")
        return job.id

    def trigger_datasource_refresh(self, datasource_id: str):
        """Triggers an extract refresh for a specific datasource."""
        logger.info(f"Triggering refresh for datasource: {datasource_id}")
        datasource = self.server.datasources.get_by_id(datasource_id)
        job = self.server.datasources.refresh(datasource)
        logger.info(f"Refresh job created: {job.id}")
        return job.id

    def wait_for_job(self, job_id: str, timeout: int = 600, interval: int = 10):
        """Waits for a Tableau background job to complete."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            job = self.server.jobs.get_by_id(job_id)
            logger.info(f"Job {job_id} status: {job.finish_code} (Progress: {job.progress}%)")
            
            if job.finish_code == '0':  # Success
                logger.info(f"Job {job_id} completed successfully.")
                return True
            elif job.finish_code == '1':  # Error
                logger.error(f"Job {job_id} failed.")
                return False
            
            time.sleep(interval)
        
        logger.error(f"Job {job_id} timed out after {timeout} seconds.")
        return False
