import tableauserverclient as TSC
from .config import TableauConfig
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TableauBaseClient:
    def __init__(self, config: TableauConfig):
        self.config = config
        self.tableau_auth = TSC.PersonalAccessTokenAuth(
            token_name=config.token_name,
            personal_access_token=config.token_value,
            site_id=config.site_name
        )
        self.server = TSC.Server(config.server_url, use_server_version=True)

    def __enter__(self):
        self.server.auth.sign_in(self.tableau_auth)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.server.auth.sign_out()

    def get_project_id(self, project_name: str) -> str:
        all_projects, pagination_item = self.server.projects.get()
        for project in all_projects:
            if project.name == project_name:
                return project.id
        raise ValueError(f"Project '{project_name}' not found.")
