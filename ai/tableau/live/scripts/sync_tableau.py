import os
import sys
import logging
from ai.tableau.live.models.connection_config import TableauConnectionConfig
from ai.tableau.live.engines.connectivity_validator import WarehouseConnectivityValidator

logger = logging.getLogger("esoteric_bank.tableau.sync")

def sync_tableau_runtime():
    """
    Orchestrates the synchronization between the institutional warehouse and Tableau.
    Ensures local Tableau Desktop can connect with the correct institutional credentials.
    """
    print("--- ESOTERIC Tableau Runtime Sync ---")
    
    # 1. Load institutional configuration
    user = os.getenv("DB_USER", "esoteric_admin")
    database = os.getenv("DB_NAME", "esoteric_bank")
    host = os.getenv("DB_HOST", "localhost")
    password = os.getenv("DB_PASSWORD", "governance_secret_2026")
    
    config = TableauConnectionConfig(
        username=user,
        database=database,
        server=host,
        password=password
    )
    
    # 2. Validate connectivity
    validator = WarehouseConnectivityValidator(config)
    if not validator.validate_connection():
        print("[CRITICAL] Cannot establish institutional sync. Aborting.")
        sys.exit(1)
        
    # 3. Output Tableau TDS Connection Data
    print(f"\n--- Institutional Datasource Details ---")
    print(f"Datasource Name : {config.datasource_name}")
    print(f"PostgreSQL Server: {config.server}:{config.port}")
    print(f"Database        : {config.database}")
    print(f"Institutional ID : {config.username}")
    print(f"SSL Mode        : {config.ssl_mode}")
    print("------------------------------------------")
    print("[SUCCESS] Institutional analytics bridge is active.")

if __name__ == "__main__":
    sync_tableau_runtime()
