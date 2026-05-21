import os
import logging
import time
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

load_dotenv()
logger = logging.getLogger("src.db")

_DEGRADED_MODE = False

def get_engine(retries=3, delay=1):
    """
    Returns a hardened SQLAlchemy engine with optimized connection pooling.
    Implements a fail-safe retry mechanism for institutional resilience.
    Supports environment-aware fallback for local development.
    """
    global _DEGRADED_MODE
    
    env = os.environ.get("ENVIRONMENT", "development")
    url = os.environ.get("DWH_URL") or os.environ.get("DATABASE_URL")
    
    # Environment-aware resolution
    if not url or (env == "development" and "db:" in url):
        if not _DEGRADED_MODE:
            logger.warning("No valid database URL found. Entering INSTITUTIONAL DEGRADED MODE (Local Fallback).")
            _DEGRADED_MODE = True
        return None

    if _DEGRADED_MODE:
        return None
    
    # ... rest of connection logic ...
    for attempt in range(retries):
        try:
            engine = create_engine(
                url, 
                future=True,
                pool_size=20,
                max_overflow=10,
                pool_timeout=30,
                pool_recycle=1800,
                pool_pre_ping=True
            )
            # Connectivity Smoke Test
            with engine.connect() as conn:
                pass
            return engine
        except OperationalError as e:
            if attempt < retries - 1:
                logger.warning(f"Database connection attempt {attempt + 1} failed. Retrying in {delay}s...")
                time.sleep(delay)
            else:
                if env == "production":
                    logger.error("Final database connection attempt failed. Institutional runtime stability compromised.")
                    raise e
                else:
                    logger.warning("Database unavailable. Falling back to DEGRADED MODE to preserve runtime stability.")
                    _DEGRADED_MODE = True
                    return None
