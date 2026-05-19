import os
import psycopg2
from psycopg2 import sql
import logging

from ai.tableau.runtime.config import TableauConfig

# Configuration from environment or TableauConfig
config = TableauConfig()
DB_URL = os.getenv("DATABASE_URL", config.pg_connection_string)
SQL_FILE_PATH = "ai/tableau/views/kpi_intelligence_views.sql"
GOVERNANCE_SQL_PATH = "ai/tableau/governance/governance_schema.sql"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("intelligence.deployer")

def deploy_kpi_views():
    """
    Deploys institutional KPI views and governance schema.
    """
    for sql_path in [GOVERNANCE_SQL_PATH, SQL_FILE_PATH]:
        if not os.path.exists(sql_path):
            logger.error(f"SQL file not found at {sql_path}")
            continue

        try:
            logger.info(f"Connecting to ESOTERIC Intelligence Warehouse to deploy {sql_path}...")
            conn = psycopg2.connect(DB_URL)
            conn.autocommit = True
            cursor = conn.cursor()

            with open(sql_path, 'r') as f:
                sql_script = f.read()

            logger.info(f"Executing SQL script from {sql_path}...")
            cursor.execute(sql_script)
            
            logger.info(f"SQL script {sql_path} deployed successfully.")
            
            cursor.close()
            conn.close()

        except Exception as e:
            logger.error(f"Failed to deploy {sql_path}: {str(e)}")

    try:
        conn = psycopg2.connect(DB_URL)
        cursor = conn.cursor()
        # Verify deployment
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.views 
            WHERE table_schema = 'intelligence';
        """)
        views = cursor.fetchall()
        logger.info(f"Deployed Intelligence Views: {[v[0] for v in views]}")

        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'governance';
        """)
        tables = cursor.fetchall()
        logger.info(f"Deployed Governance Tables: {[t[0] for t in tables]}")

        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"Verification failed: {str(e)}")

if __name__ == "__main__":
    deploy_kpi_views()
