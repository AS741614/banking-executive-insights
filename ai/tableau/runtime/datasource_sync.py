import logging
from .base_client import TableauBaseClient, TSC
from .config import TableauConfig

logger = logging.getLogger(__name__)

class DatasourceSync(TableauBaseClient):
    """
    Synchronizes PostgreSQL data sources with Tableau Server/Online.
    Ensures connection metadata is consistent.
    """

    def update_datasource_connection(self, datasource_id: str):
        """Updates the database connection details for a datasource."""
        datasource = self.server.datasources.get_by_id(datasource_id)
        self.server.datasources.populate_connections(datasource)
        
        for connection in datasource.connections:
            logger.info(f"Updating connection {connection.id} for datasource {datasource_id}")
            connection.server_address = self.config.db_host
            connection.server_port = str(self.config.db_port)
            connection.username = self.config.db_user
            connection.password = self.config.db_pass
            self.server.datasources.update_connection(datasource, connection)
            logger.info(f"Successfully updated connection to {self.config.db_host}:{self.config.db_port}")

    def sync_all_in_project(self, project_id: str):
        """Syncs all datasources within a specific project."""
        req_option = TSC.RequestOptions()
        req_option.filter.add(TSC.Filter(TSC.Filter.Operator.Equals, TSC.Filter.Field.ProjectId, project_id))
        
        all_datasources, pagination_item = self.server.datasources.get(req_option)
        logger.info(f"Syncing {len(all_datasources)} datasources in project {project_id}")
        
        for ds in all_datasources:
            try:
                self.update_datasource_connection(ds.id)
            except Exception as e:
                logger.error(f"Failed to sync datasource {ds.id}: {e}")
