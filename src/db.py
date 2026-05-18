import os
import logging
import time
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

load_dotenv()
logger = logging.getLogger("src.db")

def get_engine(retries=5, delay=2):
    """
    Returns a hardened SQLAlchemy engine with optimized connection pooling.
    Implements a fail-safe retry mechanism for institutional resilience.
    """
    url = os.environ["DWH_URL"]
    
    # Enhanced Connection Pooling for Enterprise Stability
    # - pool_size: 20 connections per process
    # - max_overflow: 10 extra connections
    # - pool_timeout: 30s before failing
    # - pool_recycle: 1800s to prevent stale connections
    # - pool_pre_ping: Validates connection before each use (Essential for transient failures)
    
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
                logger.error("Final database connection attempt failed. Institutional runtime stability compromised.")
                raise e
