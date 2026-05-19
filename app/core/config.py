import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "ESOTERIC BANK Intelligence Platform"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")
    VERSION: str = "1.0.0"
    
    # Security & JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    REFRESH_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", "1440"))
    
    # RBAC
    RBAC_POLICY_FILE: str = os.getenv("RBAC_POLICY_FILE", "infra/config/rbac_policy.yaml")
    
    # Gemini CLI settings
    GEMINI_CLI_PATH: str = os.getenv("GEMINI_CLI_PATH", "gemini")
    COGNITION_TIMEOUT_SEC: int = int(os.getenv("COGNITION_TIMEOUT_SEC", "60"))
    
    # Telemetry
    PROMETHEUS_METRICS_ENABLED: bool = os.getenv("PROMETHEUS_METRICS_ENABLED", "True").lower() in ("true", "1", "yes")
    
    # Paths
    BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    DATA_DIR: str = os.path.join(BASE_DIR, "data")
    LOGS_DIR: str = os.path.join(BASE_DIR, "logs")

    class Config:
        case_sensitive = True

settings = Settings()