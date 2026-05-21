import os
import psycopg2
import logging
from datetime import datetime, timedelta

# Configuration
DB_URL = os.getenv("DATABASE_URL", "postgresql://esoteric_admin:governance_secret_2026@localhost:5432/esoteric_bank")
STALENESS_THRESHOLD_DAYS = 90

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("tableau.governance.staleness")

class StaleDashboardDetector:
    """
    Identifies and flags analytical assets that are no longer providing institutional value.
    """
    
    def __init__(self, db_url):
        self.db_url = db_url

    def detect_stale_assets(self):
        """
        Queries the usage registry to find dashboards with zero recent engagement.
        """
        try:
            conn = psycopg2.connect(self.db_url)
            cursor = conn.cursor()

            logger.info(f"Scanning for Stale Dashboards (Threshold: {STALENESS_THRESHOLD_DAYS} days)...")

            query = """
                SELECT 
                    i.dashboard_name, 
                    i.owner_email, 
                    MAX(u.accessed_at) as last_access
                FROM governance.dashboard_inventory i
                LEFT JOIN governance.dashboard_usage u ON i.dashboard_id = u.dashboard_id
                GROUP BY 1, 2
                HAVING MAX(u.accessed_at) < CURRENT_DATE - INTERVAL '%s days'
                   OR MAX(u.accessed_at) IS NULL;
            """
            
            cursor.execute(query, (STALENESS_THRESHOLD_DAYS,))
            stale_dashboards = cursor.fetchall()

            if stale_dashboards:
                logger.warning(f"Found {len(stale_dashboards)} stale assets:")
                for name, owner, last_access in stale_dashboards:
                    last_access_str = last_access.strftime('%Y-%m-%d') if last_access else 'NEVER'
                    logger.warning(f"  - {name} (Owner: {owner}) | Last Access: {last_access_str}")
                    # In a production system, this would trigger a cleanup workflow or owner notification
            else:
                logger.info("No stale dashboards detected. All assets active within threshold.")

            cursor.close()
            conn.close()

        except Exception as e:
            logger.error(f"Staleness detection failed: {str(e)}")

if __name__ == "__main__":
    detector = StaleDashboardDetector(DB_URL)
    detector.detect_stale_assets()
