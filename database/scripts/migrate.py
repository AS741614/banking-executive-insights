import os
import sys
import psycopg2
import logging

logger = logging.getLogger("esoteric_bank.database.migrator")

class DatabaseMigrator:
    """
    Institutional Database Migrator.
    Orchestrates execution of foundational SQL schema and transformation scripts.
    """

    def __init__(self, db_url: str = None, sql_dir: str = "sql"):
        self.db_url = db_url or os.getenv("DATABASE_URL", "postgresql://esoteric_admin:governance_secret_2026@localhost:5432/esoteric_bank")
        self.sql_dir = sql_dir
        self.migration_scripts = [
            "01_schema.sql",
            "02_transform.sql",
            "03_analytics.sql",
            "04_data_quality.sql",
            "05_institutional_governance.sql"
        ]

    def execute_migrations(self):
        print("--- Initiating Institutional Migrations ---")
        try:
            conn = psycopg2.connect(self.db_url)
            conn.autocommit = True
            cur = conn.cursor()
            
            for script in self.migration_scripts:
                script_path = os.path.join(self.sql_dir, script)
                if os.path.exists(script_path):
                    print(f"[PROCESS] Executing: {script}")
                    with open(script_path, 'r') as f:
                        cur.execute(f.read())
                    print(f"[OK] Completed: {script}")
                else:
                    print(f"[WARN] Script not found: {script_path}")
            
            cur.close()
            conn.close()
            print("\n[SUCCESS] All migrations executed successfully.")
        except Exception as e:
            print(f"[CRITICAL] Migration execution failed: {e}")
            sys.exit(1)

if __name__ == "__main__":
    migrator = DatabaseMigrator()
    migrator.execute_migrations()
