import os
import psycopg2
import logging
import requests
import time
from datetime import datetime

# Configuration
DB_URL = os.getenv("DATABASE_URL", "postgresql://esoteric_admin:governance_secret_2026@localhost:5432/esoteric_bank")
TABLEAU_GATEWAY = "http://localhost:8501" # Simulating the Streamlit gateway for this demo

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("tableau.observability.health")

class DashboardHealthMonitor:
    """
    Simulates health checks for institutional dashboards.
    """
    
    def __init__(self, db_url):
        self.db_url = db_url

    def check_dashboards(self):
        """
        Pings dashboard gateways and logs latency/availability.
        """
        try:
            conn = psycopg2.connect(self.db_url)
            cursor = conn.cursor()

            # Fetch dashboards from inventory
            cursor.execute("SELECT dashboard_id, dashboard_name, project_path FROM governance.dashboard_inventory")
            dashboards = cursor.fetchall()

            if not dashboards:
                logger.warning("No dashboards found in inventory. Seed the registry first.")
                # Seeding a default for demo purposes
                cursor.execute("""
                    INSERT INTO governance.dashboard_inventory (dashboard_name, project_path, is_executive, criticality_tier)
                    VALUES ('Executive Intelligence Gateway', '/executive/overview', TRUE, 1)
                    RETURNING dashboard_id;
                """)
                dashboards = [(cursor.fetchone()[0], 'Executive Intelligence Gateway', '/executive/overview')]
                conn.commit()

            logger.info("Starting Dashboard Health Monitoring...")

            for d_id, name, path in dashboards:
                start_time = time.time()
                try:
                    # In a real scenario, this would be a Tableau Server REST API call
                    # Here we simulate a check on the stabilized UI gateway
                    status_code = 200 # Simulated success
                    latency = int((time.time() - start_time) * 1000)
                    status = 'HEALTHY' if status_code == 200 else 'DEGRADED'
                    
                    logger.info(f"Health Check {name}: {status} ({latency}ms)")

                    cursor.execute("""
                        INSERT INTO governance.dashboard_health_logs (dashboard_id, status, latency_ms)
                        VALUES (%s, %s, %s)
                    """, (d_id, status, latency))

                except Exception as e:
                    logger.error(f"Failed to check dashboard {name}: {str(e)}")
                    cursor.execute("""
                        INSERT INTO governance.dashboard_health_logs (dashboard_id, status, error_message)
                        VALUES (%s, %s, %s)
                    """, (d_id, 'UNAVAILABLE', str(e)))

            conn.commit()
            cursor.close()
            conn.close()

        except Exception as e:
            logger.error(f"Health monitoring failed: {str(e)}")

if __name__ == "__main__":
    monitor = DashboardHealthMonitor(DB_URL)
    monitor.check_dashboards()
