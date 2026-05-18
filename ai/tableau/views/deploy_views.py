import os
import psycopg2
from psycopg2 import sql
import logging

# Configuration from environment
DB_URL = os.getenv("DATABASE_URL", "postgresql://esoteric_admin:governance_secret_2026@localhost:5432/esoteric_bank")
SQL_FILE_PATH = "ai/tableau/views/kpi_intelligence_views.sql"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("intelligence.deployer")

def deploy_kpi_views():
    """
    Deploys institutional KPI views to the PostgreSQL intelligence schema.
    """
    if not os.path.exists(SQL_FILE_PATH):
        logger.error(f"SQL file not found at {SQL_FILE_PATH}")
        return

    try:
        logger.info("Connecting to ESOTERIC Intelligence Warehouse...")
        conn = psycopg2.connect(DB_URL)
        conn.autocommit = True
        cursor = conn.cursor()

        with open(SQL_FILE_PATH, 'r') as f:
            sql_script = f.read()

        logger.info("Executing KPI View Generation Script...")
        # Split script by semicolon to execute commands individually if needed, 
        # or execute as one block. For views/mviews, one block is usually fine.
        cursor.execute(sql_script)
        
        logger.info("KPI Intelligence Views deployed successfully.")
        
        # Verify deployment
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.views 
            WHERE table_schema = 'intelligence';
        """)
        views = cursor.fetchall()
        logger.info(f"Deployed Views: {[v[0] for v in views]}")

        cursor.close()
        conn.close()

    except Exception as e:
        logger.error(f"Failed to deploy KPI views: {str(e)}")

if __name__ == "__main__":
    deploy_kpi_views()
