import logging
import pandas as pd
import pantab
from sqlalchemy import create_engine
from .base_client import TableauBaseClient, TSC
from .config import TableauConfig

logger = logging.getLogger(__name__)

class HyperOrchestrator(TableauBaseClient):
    """
    Orchestrates the extraction of data from PostgreSQL to Hyper files
    and publishing to Tableau Server/Online.
    """

    def export_to_hyper(self, query: str, hyper_path: str, table_name: str = "Extract"):
        """Executes a SQL query and exports the result to a Hyper file."""
        logger.info(f"Executing query for Hyper export: {query[:100]}...")
        engine = create_engine(self.config.pg_connection_string)
        df = pd.read_sql(query, engine)
        
        logger.info(f"Writing {len(df)} rows to {hyper_path}")
        pantab.frame_to_hyper(df, hyper_path, table=table_name)
        logger.info("Hyper file generated successfully.")

    def publish_hyper(self, hyper_path: str, datasource_name: str, project_id: str):
        """Publishes a Hyper file as a datasource to Tableau."""
        logger.info(f"Publishing {hyper_path} as {datasource_name} to project {project_id}")
        
        new_datasource = TSC.DatasourceItem(project_id, name=datasource_name)
        new_datasource = self.server.datasources.publish(
            new_datasource, hyper_path, TSC.Server.PublishMode.Overwrite
        )
        logger.info(f"Successfully published datasource: {new_datasource.id}")
        return new_datasource.id

    def run_pipeline(self, query: str, datasource_name: str, hyper_filename: str):
        """Full pipeline: SQL -> Hyper -> Publish."""
        hyper_path = f"tableau/exports/{hyper_filename}"
        self.export_to_hyper(query, hyper_path)
        
        with self:
            project_id = self.config.project_id
            if not project_id:
                project_id = self.get_project_id("Banking Insights")
            
            return self.publish_hyper(hyper_path, datasource_name, project_id)
