import requests
import os
import json
import logging
import subprocess
from typing import Dict, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("deployment.validator")

class DeploymentValidator:
    """
    Executes production-grade deployment validation for the ESOTERIC platform.
    """
    
    def __init__(self, api_url: str = "http://localhost:8000", ui_url: str = "http://localhost:8501"):
        self.api_url = api_url
        self.ui_url = ui_url

    def validate_docker_topology(self) -> Dict[str, Any]:
        """Audits the running Docker containers."""
        logger.info("Auditing Docker Topology...")
        try:
            result = subprocess.run(
                ["docker", "compose", "-f", "docker-compose.enterprise.yml", "ps", "--format", "json"],
                capture_output=True, text=True, check=True
            )
            # Handle potential multi-line json output
            containers = [json.loads(line) for line in result.stdout.strip().split('\n') if line]
            
            report = {"status": "SUCCESS", "containers": []}
            for container in containers:
                status = container.get("Status", container.get("State", "UNKNOWN"))
                logger.info(f"Container {container['Name']}: {status}")
                if "Up" not in status and "running" not in status:
                    report["status"] = "DEGRADED"
                report["containers"].append({
                    "name": container["Name"],
                    "service": container["Service"],
                    "status": status
                })
            return report
        except Exception as e:
            logger.error(f"Docker audit failed: {e}")
            return {"status": "FAILED", "error": str(e)}

    def validate_fastapi_runtime(self) -> Dict[str, Any]:
        """Validates the API health and institutional status."""
        logger.info("Validating FastAPI Runtime...")
        # Include a check for the ECOS kernel status if available
        endpoints = ["/health", "/api/v1/platform/status"]
        report = {"status": "SUCCESS", "checks": []}
        
        for ep in endpoints:
            try:
                resp = requests.get(f"{self.api_url}{ep}", timeout=5)
                status = "PASSED" if resp.status_code == 200 else "FAILED"
                logger.info(f"Endpoint {ep}: {status}")
                
                # Check for kernel status in platform/status response
                if ep == "/api/v1/platform/status" and status == "PASSED":
                    data = resp.json().get("data", {})
                    kernel_status = data.get("kernel_status", "UNKNOWN")
                    logger.info(f"ECOS Kernel Status: {kernel_status}")
                    report["checks"].append({"endpoint": "ecos_kernel", "status": "PASSED" if kernel_status == "READY" else "DEGRADED"})

                if status == "FAILED": report["status"] = "DEGRADED"
                report["checks"].append({"endpoint": ep, "status": status, "code": resp.status_code})
            except Exception as e:
                report["status"] = "DEGRADED"
                report["checks"].append({"endpoint": ep, "status": "ERROR", "error": str(e)})
        return report

    def validate_streamlit_gateway(self) -> Dict[str, Any]:
        """Validates the UI gateway accessibility."""
        logger.info("Validating Streamlit Gateway...")
        try:
            # Streamlit health check
            resp = requests.get(f"{self.ui_url}/_stcore/health", timeout=5)
            status = "PASSED" if resp.status_code == 200 else "FAILED"
            logger.info(f"UI Gateway: {status}")
            return {"status": status, "code": resp.status_code}
        except Exception as e:
            logger.error(f"UI validation failed: {e}")
            return {"status": "ERROR", "error": str(e)}

    def run_full_audit(self):
        """Runs the complete deployment audit and generates a report."""
        print("\n" + "="*60)
        print("ESOTERIC BANK - DEPLOYMENT VALIDATION AUDIT")
        print("="*60)
        
        docker_res = self.validate_docker_topology()
        api_res = self.validate_fastapi_runtime()
        ui_res = self.validate_streamlit_gateway()
        
        overall_status = "STABLE" if all(r["status"] in ["SUCCESS", "PASSED"] for r in [docker_res, api_res, ui_res]) else "UNSTABLE"
        
        print(f"\nOVERALL DEPLOYMENT STATUS: [{overall_status}]")
        
        print("\n[1. DOCKER TOPOLOGY]")
        for c in docker_res.get("containers", []):
            print(f"  - {c['name']} ({c['service']}): {c['status']}")
            
        print("\n[2. API RUNTIME]")
        for check in api_res.get("checks", []):
            print(f"  - {check['endpoint']}: {check['status']}")
            
        print("\n[3. UI GATEWAY]")
        print(f"  - Status: {ui_res['status']}")
        
        print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    validator = DeploymentValidator()
    validator.run_full_audit()
