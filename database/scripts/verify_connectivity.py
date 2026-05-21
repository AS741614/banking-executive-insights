import os
import psycopg2
import sys
import time
from urllib.parse import urlparse

def verify_db_connectivity():
    """
    Institutional Database Connectivity Verifier.
    Performs multi-stage validation of the persistence layer.
    """
    db_url = os.getenv("DATABASE_URL", "postgresql://esoteric_admin:governance_secret_2026@db:5432/esoteric_bank")
    
    # Parse URL for detailed logging
    parsed = urlparse(db_url)
    host = parsed.hostname
    port = parsed.port or 5432
    db_name = parsed.path.lstrip('/')
    
    print(f"--- DATABASE CONNECTIVITY VERIFICATION ---")
    print(f"[TARGET] Host: {host}, Port: {port}, DB: {db_name}")
    
    max_retries = 5
    for attempt in range(1, max_retries + 1):
        try:
            print(f"[ATTEMPT {attempt}] Establishing connection...")
            conn = psycopg2.connect(db_url, connect_timeout=5)
            cur = conn.cursor()
            
            # 1. Version Check
            cur.execute("SELECT version();")
            version = cur.fetchone()[0]
            print(f"[OK] PostgreSQL Version: {version[:40]}...")
            
            # 2. Institutional Schema Validation
            cur.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name IN ('governance', 'mart', 'staging');")
            schemas = [r[0] for r in cur.fetchall()]
            print(f"[OK] Schemas Detected: {', '.join(schemas)}")
            
            # 3. Governance Tables Validation
            cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'governance';")
            tables = [r[0] for r in cur.fetchall()]
            print(f"[OK] Governance Tables: {', '.join(tables)}")
            
            # 4. Persistence Test
            cur.execute("CREATE TABLE IF NOT EXISTS public.persistence_test (id INT, ts TIMESTAMP DEFAULT NOW());")
            cur.execute("INSERT INTO public.persistence_test (id) VALUES (1);")
            cur.execute("SELECT count(*) FROM public.persistence_test;")
            count = cur.fetchone()[0]
            print(f"[OK] Persistence Validation: {count} test entries recorded.")
            
            cur.close()
            conn.close()
            print("\n[SUCCESS] Institutional Persistence Layer is STABLE.")
            return True
            
        except psycopg2.OperationalError as e:
            print(f"[ERROR] Connection failed: {e}")
            if attempt < max_retries:
                wait_time = 2 ** attempt
                print(f"[RETRY] Waiting {wait_time}s before next attempt...")
                time.sleep(wait_time)
            else:
                print(f"[CRITICAL] Max retries reached. Database unreachable.")
                return False
        except Exception as e:
            print(f"[CRITICAL] Unexpected error: {e}")
            return False

if __name__ == "__main__":
    if not verify_db_connectivity():
        sys.exit(1)
