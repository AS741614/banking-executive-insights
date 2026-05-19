from pydantic import BaseModel, Field
from typing import Optional

class TableauConnectionConfig(BaseModel):
    """
    Institutional Tableau Connection Configuration.
    Maps PostgreSQL warehouse parameters to Tableau-compatible DSN settings.
    """
    server: str = Field(default="localhost")
    port: int = Field(default=5432)
    database: str = Field(default="bank_dwh")
    username: str = Field(default="dwh")
    password: str = Field(default="dwh")
    ssl_mode: str = Field(default="prefer")
    
    # Tableau specific metadata
    datasource_name: str = Field(default="ESOTERIC_WAREHOUSE_LIVE")
    refresh_interval_min: int = Field(default=15)
    authentication_method: str = Field(default="username-password")

    @property
    def connection_url(self) -> str:
        return f"postgresql://{self.username}:{self.password}@{self.server}:{self.port}/{self.database}"
