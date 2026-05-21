import os
import psycopg2
import logging
from datetime import datetime

# Configuration
DB_URL = os.getenv("DATABASE_URL", "postgresql://esoteric_admin:governance_secret_2026@localhost:5432/esoteric_bank")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("tableau.governance.reporter")

class GovernanceReporter:
    """
    Generates institutional governance intelligence reports for the Executive Command Center.
    """
    
    def __init__(self, db_url):
        self.db_url = db_url

    def generate_report(self):
        """
        Aggregates monitoring and governance logs into a comprehensive summary.
        """
        try:
            conn = psycopg2.connect(self.db_url)
            cursor = conn.cursor()

            report = {
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "health_summary": {},
                "drift_anomalies": [],
                "datasource_status": {},
                "staleness_count": 0
            }

            # 1. Dashboard Health Summary
            cursor.execute("""
                SELECT status, COUNT(*) 
                FROM governance.dashboard_health_logs 
                WHERE checked_at > CURRENT_TIMESTAMP - INTERVAL '24 hours'
                GROUP BY 1
            """)
            report["health_summary"] = dict(cursor.fetchall())

            # 2. Critical KPI Drift Anomalies
            cursor.execute("""
                SELECT kpi_name, dimension_scope, drift_percentage 
                FROM governance.kpi_drift_log 
                WHERE is_anomaly = TRUE 
                AND detected_at > CURRENT_TIMESTAMP - INTERVAL '24 hours'
            """)
            report["drift_anomalies"] = cursor.fetchall()

            # 3. Datasource Status
            cursor.execute("""
                SELECT datasource_name, drift_status 
                FROM governance.datasource_metrics
            """)
            report["datasource_status"] = dict(cursor.fetchall())

            # 4. Stale Asset Count
            cursor.execute("""
                SELECT COUNT(*) 
                FROM governance.dashboard_inventory i
                LEFT JOIN governance.dashboard_usage u ON i.dashboard_id = u.dashboard_id
                HAVING MAX(u.accessed_at) < CURRENT_DATE - INTERVAL '90 days'
                   OR MAX(u.accessed_at) IS NULL;
            """)
            staleness = cursor.fetchone()
            report["staleness_count"] = staleness[0] if staleness else 0

            # --- Output Generation ---
            print("\n" + "="*60)
            print(f"ESOTERIC BANK - TABLEAU GOVERNANCE INTELLIGENCE REPORT")
            print(f"Generated: {report['timestamp']}")
            print("="*60)

            print(f"\n[DASHBOARD HEALTH (24H)]")
            for status, count in report["health_summary"].items():
                print(f"  - {status}: {count}")

            print(f"\n[CRITICAL KPI DRIFT]")
            if not report["drift_anomalies"]:
                print("  - No anomalies detected.")
            else:
                for kpi, scope, drift in report["drift_anomalies"]:
                    print(f"  - ALERT: {kpi} ({scope}) drifted {drift:.2f}%")

            print(f"\n[DATASOURCE OBSERVABILITY]")
            for ds, status in report["datasource_status"].items():
                print(f"  - {ds}: {status}")

            print(f"\n[ASSET LIFECYCLE]")
            print(f"  - Stale Dashboards Detected: {report['staleness_count']}")
            print("="*60 + "\n")

            cursor.close()
            conn.close()

        except Exception as e:
            logger.error(f"Governance reporting failed: {str(e)}")

if __name__ == "__main__":
    reporter = GovernanceReporter(DB_URL)
    reporter.generate_report()
