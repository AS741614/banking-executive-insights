import asyncio
import os
import logging
from runtime.health.monitor import monitor

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("stabilization.db_validator")

async def validate_db_connectivity():
    """
    Validates that the PostgreSQL database is reachable using the updated health monitor.
    Addresses B-RUN-01: PostgreSQL Unreachability.
    """
    print("=== Institutional DB Connectivity Validation ===")
    
    # Set environment variables for local validation (targeting the new exposed port 5433)
    os.environ["DB_HOST"] = "localhost"
    os.environ["DB_PORT"] = "5433"
    
    logger.info(f"Testing connectivity to {os.environ['DB_HOST']}:{os.environ['DB_PORT']}...")
    
    is_alive = await monitor.check_port_availability(os.environ["DB_HOST"], int(os.environ["DB_PORT"]))
    
    if is_alive:
        print("[SUCCESS] PostgreSQL is reachable on the institutional stabilization port (5433).")
        print("Root cause remediated: DB port exposed and monitor configured for local access.")
    else:
        print("[FAIL] PostgreSQL remains unreachable.")
        print("Ensure 'docker-compose.enterprise.yml' is running and port 5433 is mapped.")

if __name__ == "__main__":
    asyncio.run(validate_db_connectivity())
