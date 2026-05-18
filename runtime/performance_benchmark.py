import asyncio
import time
import httpx
import statistics
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("esoteric_bank.runtime.benchmark")

class InstitutionalPerformanceHardener:
    """
    Enterprise Performance Hardener.
    Validates async runtime resilience and API latency thresholds.
    """

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.latencies = []

    async def probe_latency(self, client: httpx.AsyncClient):
        start = time.time()
        try:
            response = await client.get(f"{self.base_url}/health")
            if response.status_code == 200:
                self.latencies.append((time.time() - start) * 1000)
        except Exception as e:
            logger.error(f"Probe failed: {e}")

    async def execute_stress_validation(self, concurrent_requests: int = 50):
        """
        Executes a burst of concurrent requests to validate async stability.
        """
        logger.info(f"Initiating institutional stress validation: {concurrent_requests} concurrent probes.")
        
        async with httpx.AsyncClient() as client:
            tasks = [self.probe_latency(client) for _ in range(concurrent_requests)]
            await asyncio.gather(*tasks)

        if not self.latencies:
            logger.error("No successful probes recorded. Runtime unstable.")
            return False

        avg_lat = statistics.mean(self.latencies)
        p95_lat = statistics.quantiles(self.latencies, n=20)[18] # 95th percentile
        
        logger.info(f"--- Performance Report ---")
        logger.info(f"Average Latency: {avg_lat:.2f}ms")
        logger.info(f"P95 Latency    : {p95_lat:.2f}ms")
        logger.info(f"Resilience Status: [{'STABLE' if p95_lat < 100 else 'DEGRADED'}]")
        
        return p95_lat < 200 # Institutional threshold

if __name__ == "__main__":
    hardener = InstitutionalPerformanceHardener()
    loop = asyncio.get_event_loop()
    success = loop.run_until_complete(hardener.execute_stress_validation())
    if not success:
        logger.warning("Runtime failed performance thresholds. Optimization required.")
        exit(1)
