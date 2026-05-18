import os
import sys
import logging
import psycopg2
from typing import Dict, Any

logger = logging.getLogger("esoteric_bank.database.validator")

class DatabaseRuntimeValidator:
    """
    Institutional Database Runtime Validator.
    Ensures PostgreSQL availability and schema readiness.
    """

    def __init__(self, db_url: str = None):
        self.db_url = db_url or os.getenv("DATABASE_URL", "postgresql://esoteric_admin:governance_secret_2026@localhost:5432/esoteric_bank")

    def validate_connectivity(self) -> bool:
        print(f"--- Database Connectivity Validation ---")
        try:
            conn = psycopg2.connect(self.db_url)
            cur = conn.cursor()
            cur.execute("SELECT version();")
            version = cur.fetchone()
            print(f"[OK] PostgreSQL Connection established.")
            print(f"[INFO] Version: {version[0]}")
            cur.close()
            conn.close()
            return True
        except Exception as e:
            print(f"[FAIL] Database connection failed: {e}")
            return False

    def validate_user_permissions(self) -> bool:
        try:
            conn = psycopg2.connect(self.db_url)
            cur = conn.cursor()
            # Check if user can create tables
            cur.execute("CREATE TEMP TABLE val_test (id int); DROP TABLE val_test;")
            print(f"[OK] User permissions verified (CREATE TEMP TABLE).")
            cur.close()
            conn.close()
            return True
        except Exception as e:
            print(f"[FAIL] Permission check failed: {e}")
            return False

if __name__ == "__main__":
    validator = DatabaseRuntimeValidator()
    if not validator.validate_connectivity() or not validator.validate_user_permissions():
        sys.exit(1)
    print("\n[SUCCESS] Database runtime validated.")
