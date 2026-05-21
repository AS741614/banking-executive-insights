import asyncio
import logging
import socket
import os
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger("ecos.runtime.health.monitor")

class ServiceHealthMonitor:
    """
    Advanced runtime health monitor for institutional service resilience.
    Detects failures and triggers circuit breaker patterns if necessary.
    """
    
    def __init__(self):
        self._health_registry: Dict[str, Dict[str, Any]] = {}
        self._failure_threshold = 3

    async def check_port_availability(self, host: str, port: int) -> bool:
        """
        Checks if a TCP port is reachable.
        """
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(host, port),
                timeout=1.0
            )
            writer.close()
            await writer.wait_closed()
            return True
        except Exception:
            return False

    async def monitor_institutional_stack(self):
        """
        Orchestrates health checks across the core enterprise stack.
        """
        logger.info("Initializing institutional stack health monitoring...")
        
        # 1. Environment and Runtime Mode Resolution
        env = os.getenv("ENVIRONMENT", "development")
        runtime_mode = os.getenv("RUNTIME_MODE", "auto") # auto, local, docker, hybrid, frontend-only
        
        # 2. Database Resolution Strategy
        db_url = os.getenv("DATABASE_URL")
        db_host = os.getenv("DB_HOST")
        db_port = int(os.getenv("DB_PORT", "5432"))

        # Automatic resolution if not explicitly set
        if not db_host:
            if runtime_mode == "docker":
                db_host = "db"
            elif runtime_mode == "local":
                db_host = "localhost"
            else:
                db_host = "db" if env == "production" else "localhost"

        # Override from DATABASE_URL if present
        if db_url:
            from urllib.parse import urlparse
            try:
                parsed = urlparse(db_url)
                if parsed.hostname:
                    db_host = parsed.hostname
                if parsed.port:
                    db_port = parsed.port
            except Exception:
                logger.warning("Failed to parse DATABASE_URL for health monitoring.")

        # 3. Stack Definition
        stack = {
            "API Gateway": (os.getenv("API_HOST", "localhost"), int(os.getenv("API_PORT", "8000"))),
            "Next.js Experience Layer": (os.getenv("UI_HOST", "localhost"), int(os.getenv("UI_PORT", "3000")))
        }

        # Handle Intentional Degraded Mode and Frontend-Only Suppression
        intentional_degraded = not db_url or runtime_mode == "frontend-only"
        
        if runtime_mode != "frontend-only":
            stack["PostgreSQL"] = (db_host, db_port)
            if intentional_degraded:
                logger.info("Institutional persistence not configured. Monitoring in DEGRADED mode.")

        while True:
            for service, (host, port) in stack.items():
                is_alive = await self.check_port_availability(host, port)
                
                if service not in self._health_registry:
                    self._health_registry[service] = {
                        "failures": 0, 
                        "status": "UNKNOWN",
                        "last_alert_time": 0
                    }

                current_time = datetime.utcnow().timestamp()
                service_data = self._health_registry[service]

                if not is_alive:
                    service_data["failures"] += 1
                    
                    # Distinguish between intentional degraded mode vs unexpected failure
                    is_expected_unreachable = (service == "PostgreSQL" and intentional_degraded)
                    
                    if not is_expected_unreachable:
                        if service_data["failures"] <= 1 or env == "production":
                            logger.warning(f"Service {service} unreachable ({host}:{port}). Failures: {service_data['failures']}")
                    
                    # Logic for critical alerts
                    if service_data["failures"] >= self._failure_threshold and not is_expected_unreachable:
                        if service_data["status"] != "DEGRADED" or (current_time - service_data["last_alert_time"] > 3600):
                            service_data["status"] = "DEGRADED"
                            service_data["last_alert_time"] = current_time
                            logger.critical(f"Service {service} is critically DEGRADED. Triggering resilience protocols.")
                    elif is_expected_unreachable:
                        service_data["status"] = "DEGRADED_INTENTIONAL"
                else:
                    if service_data["status"] in ["DEGRADED", "DEGRADED_INTENTIONAL"]:
                        logger.info(f"Service {service} has RECOVERED/CONNECTED.")
                    service_data["failures"] = 0
                    service_data["status"] = "HEALTHY"

            await asyncio.sleep(10)

    def get_stack_health_report(self) -> Dict[str, Any]:
        """
        Returns a high-level health report for observability.
        """
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "stack": self._health_registry
        }

monitor = ServiceHealthMonitor()
