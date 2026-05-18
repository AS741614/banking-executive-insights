import logging
import sys
from .config import TableauConfig
from .health_monitor import HealthMonitor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_runtime():
    """
    Performs a comprehensive validation of the Tableau automation runtime.
    """
    logger.info("Starting Tableau Runtime Validation...")
    
    config = TableauConfig()
    monitor = HealthMonitor(config)
    
    # 1. Check Libraries
    try:
        import tableauserverclient
        import pantab
        import pandas
        import sqlalchemy
        logger.info("SUCCESS: Required libraries (TSC, pantab, pandas, sqlalchemy) are present.")
    except ImportError as e:
        logger.error(f"FAILURE: Missing library: {e}")
        return False

    # 2. Check Server Connectivity
    if monitor.check_server_health():
        logger.info("SUCCESS: Tableau Server connectivity validated.")
    else:
        logger.error("FAILURE: Could not connect to Tableau Server. Check .env settings.")
        return False

    # 3. Check DB Connectivity
    try:
        from sqlalchemy import create_engine
        engine = create_engine(config.pg_connection_string)
        with engine.connect() as conn:
            logger.info("SUCCESS: PostgreSQL connectivity validated.")
    except Exception as e:
        logger.error(f"FAILURE: Database connection failed: {e}")
        return False

    logger.info("--- Runtime Validation Passed ---")
    return True

if __name__ == "__main__":
    success = validate_runtime()
    sys.exit(0 if success else 1)
