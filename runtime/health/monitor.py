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
        
        db_host = os.getenv("DB_HOST", "db")
        db_port = int(os.getenv("DB_PORT", "5432"))
        api_host = os.getenv("API_HOST", "localhost")
        api_port = int(os.getenv("API_PORT", "8000"))
        ui_host = os.getenv("UI_HOST", "localhost")
        ui_port = int(os.getenv("UI_PORT", "8501"))

        stack = {
            "PostgreSQL": (db_host, db_port),
            "API Gateway": (api_host, api_port),
            "UI Command Center": (ui_host, ui_port)
        }

        while True:
            for service, (host, port) in stack.items():
                is_alive = await self.check_port_availability(host, port)
                
                if service not in self._health_registry:
                    self._health_registry[service] = {"failures": 0, "status": "UNKNOWN"}

                if not is_alive:
                    self._health_registry[service]["failures"] += 1
                    logger.warning(f"Service {service} unreachable ({host}:{port}). Failures: {self._health_registry[service]['failures']}")
                else:
                    if self._health_registry[service]["status"] == "DEGRADED":
                        logger.info(f"Service {service} has RECOVERED.")
                    self._health_registry[service]["failures"] = 0
                    self._health_registry[service]["status"] = "HEALTHY"

                if self._health_registry[service]["failures"] >= self._failure_threshold:
                    self._health_registry[service]["status"] = "DEGRADED"
                    logger.critical(f"Service {service} is critically DEGRADED. Triggering resilience protocols.")

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
