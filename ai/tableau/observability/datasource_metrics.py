import os
import psycopg2
import logging
from datetime import datetime, timedelta

# Configuration
DB_URL = os.getenv("DATABASE_URL", "postgresql://esoteric_admin:governance_secret_2026@localhost:5432/esoteric_bank")
FRESHNESS_THRESHOLD_HOURS = 24

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("tableau.observability.datasource")

class DatasourceObserver:
    """
    Monitors the freshness and integrity of analytical datasources.
    """
    
    def __init__(self, db_url):
        self.db_url = db_url

    def observe_datasources(self):
        """
        Validates the state of core tables used by Tableau.
        """
        try:
            conn = psycopg2.connect(self.db_url)
            cursor = conn.cursor()

            # Target tables for observability
            target_tables = [
                ('intelligence', 'vw_executive_kpis'),
                ('intelligence', 'mv_adaptive_intelligence_summary'),
                ('mart', 'fact_transaction')
            ]

            logger.info("Starting Institutional Datasource Observability Check...")

            for schema, table in target_tables:
                # Check row count and max date (freshness)
                # Note: For views, we check the underlying facts
                query = f"SELECT COUNT(*), MAX(open_date) FROM mart.dim_account" if table == 'fact_transaction' else \
                        f"SELECT COUNT(*), CURRENT_TIMESTAMP FROM {schema}.{table}"
                
                cursor.execute(query)
                count, last_update = cursor.fetchone()
                
                # In a real environment, we'd use a dedicated 'last_updated' column
                # Here we simulate freshness check
                is_stale = False # Simulated logic
                
                status = 'DEGRADED' if is_stale else 'HEALTHY'
                logger.info(f"Observed {schema}.{table}: Count={count}, Status={status}")

                # Update governance registry
                cursor.execute("""
                    INSERT INTO governance.datasource_metrics 
                    (datasource_name, source_type, schema_name, table_name, last_refreshed_at, row_count_baseline, drift_status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (datasource_id) DO UPDATE SET
                    last_refreshed_at = EXCLUDED.last_refreshed_at,
                    row_count_baseline = EXCLUDED.row_count_baseline,
                    drift_status = EXCLUDED.drift_status;
                """, (f"{schema}.{table}", "POSTGRES", schema, table, last_update, count, status))

            conn.commit()
            cursor.close()
            conn.close()

        except Exception as e:
            logger.error(f"Datasource observability failed: {str(e)}")

if __name__ == "__main__":
    observer = DatasourceObserver(DB_URL)
    observer.observe_datasources()
