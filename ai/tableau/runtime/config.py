import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class TableauConfig:
    server_url: str = os.getenv("TABLEAU_SERVER_URL", "https://prod-useast-b.online.tableau.com")
    site_name: str = os.getenv("TABLEAU_SITE_NAME", "bankinginsights")
    token_name: str = os.getenv("TABLEAU_TOKEN_NAME", "")
    token_value: str = os.getenv("TABLEAU_TOKEN_VALUE", "")
    project_id: str = os.getenv("TABLEAU_PROJECT_ID", "")
    
    # PostgreSQL Source Config
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = int(os.getenv("DB_PORT", 5432))
    db_name: str = os.getenv("DB_NAME", "bank_dwh")
    db_user: str = os.getenv("DB_USER", "dwh")
    db_pass: str = os.getenv("DB_PASS", "dwh")

    @property
    def pg_connection_string(self) -> str:
        return f"postgresql://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"
