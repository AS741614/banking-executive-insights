import os
import sys
import psycopg2
from typing import List

class WarehouseHealthChecker:
    """
    Enterprise Warehouse Health Checker.
    Validates institutional data integrity and schema existence.
    """

    def __init__(self, db_url: str = None):
        self.db_url = db_url or os.getenv("DATABASE_URL", "postgresql://esoteric_admin:governance_secret_2026@localhost:5432/esoteric_bank")
        self.critical_tables = [
            "raw_accounts", "raw_branches", "raw_customers", 
            "raw_products", "raw_transactions", "mv_kpi_month"
        ]

    def check_schema_integrity(self) -> bool:
        print("--- Warehouse Schema Integrity Check ---")
        try:
            conn = psycopg2.connect(self.db_url)
            cur = conn.cursor()
            
            missing_tables = []
            for table in self.critical_tables:
                cur.execute(f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{table}');")
                exists = cur.fetchone()[0]
                if not exists:
                    missing_tables.append(table)
                    print(f"[FAIL] Table missing: {table}")
                else:
                    cur.execute(f"SELECT COUNT(*) FROM {table};")
                    count = cur.fetchone()[0]
                    print(f"[OK] Table: {table} | Row Count: {count}")
            
            cur.close()
            conn.close()
            
            if missing_tables:
                return False
            return True
        except Exception as e:
            print(f"[ERROR] Warehouse health check failed: {e}")
            return False

if __name__ == "__main__":
    checker = WarehouseHealthChecker()
    if not checker.check_schema_integrity():
        print("\n[WARN] Warehouse schema is incomplete. Migrations may be required.")
    else:
        print("\n[SUCCESS] Warehouse health check passed.")
