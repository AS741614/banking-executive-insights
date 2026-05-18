import os
import time
import logging
import psycopg2
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("db_stabilization.readiness")

def wait_for_db(db_url: str, timeout: int = 60):
    """
    Waits for the database to be fully ready for application-level queries.
    Goes beyond 'pg_isready' by validating authentication and query execution.
    """
    start_time = time.time()
    logger.info(f"Validating database readiness: {db_url}")
    
    while time.time() - start_time < timeout:
        try:
            # Attempt connection and simple query
            engine = create_engine(db_url, connect_args={'connect_timeout': 5})
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                logger.info("[SUCCESS] Database is fully reachable and authenticated.")
                return True
        except (OperationalError, Exception) as e:
            elapsed = int(time.time() - start_time)
            logger.warning(f"Database not ready yet ({elapsed}s elapsed): {str(e)[:100]}...")
            time.sleep(2)
            
    logger.error(f"[FAIL] Database readiness validation timed out after {timeout}s.")
    return False

if __name__ == "__main__":
    db_url = os.getenv("DATABASE_URL", "postgresql://esoteric_admin:governance_secret_2026@localhost:5433/esoteric_bank")
    if not wait_for_db(db_url):
        exit(1)
