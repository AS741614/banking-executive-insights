import logging
import psycopg2
from ai.tableau.live.models.connection_config import TableauConnectionConfig

logger = logging.getLogger("esoteric_bank.tableau.connectivity_validator")

class WarehouseConnectivityValidator:
    """
    Institutional Warehouse Connectivity Validator.
    Ensures that the PostgreSQL warehouse is accessible and ready for Tableau live queries.
    """

    def __init__(self, config: TableauConnectionConfig):
        self.config = config

    def validate_connection(self) -> bool:
        print(f"--- Tableau-Warehouse Connectivity Check ---")
        try:
            conn = psycopg2.connect(
                host=self.config.server,
                port=self.config.port,
                database=self.config.database,
                user=self.config.username,
                password=self.config.password
            )
            cur = conn.cursor()
            cur.execute("SELECT current_database(), current_user, version();")
            info = cur.fetchone()
            print(f"[OK] Live connection verified to database: {info[0]}")
            print(f"[INFO] Principal: {info[1]}")
            
            # Check for critical Tableau-ready views
            cur.execute("""
                SELECT count(*) FROM (
                    SELECT table_name FROM information_schema.views WHERE table_name = 'vw_executive_kpis' AND table_schema = 'intelligence'
                    UNION
                    SELECT matviewname FROM pg_matviews WHERE matviewname = 'mv_adaptive_intelligence_summary' AND schemaname = 'intelligence'
                ) as unified_views;
            """)
            if cur.fetchone()[0] >= 2:
                print(f"[OK] Intelligence views are present.")
            else:
                print(f"[WARN] Intelligence views missing. Check deployment status.")

            cur.close()
            conn.close()
            return True
        except Exception as e:
            print(f"[CRITICAL] Connectivity validation failed: {e}")
            return False

    def validate_tableau_performance(self) -> float:
        """Simple probe to measure query latency for live dashboards."""
        import time
        try:
            conn = psycopg2.connect(
                host=self.config.server,
                port=self.config.port,
                database=self.config.database,
                user=self.config.username,
                password=self.config.password
            )
            start = time.time()
            cur = conn.cursor()
            cur.execute("SELECT count(*) FROM mart.fact_transaction;")
            cur.fetchone()
            latency = (time.time() - start) * 1000
            print(f"[INFO] Analytical Latency: {latency:.2f}ms")
            cur.close()
            conn.close()
            return latency
        except Exception:
            return -1.0
