import requests
import logging
from typing import Dict, Any

logger = logging.getLogger("esoteric_bank.runtime.api_validator")

class APIValidator:
    """
    Enterprise API Readiness & Health Validator.
    Executes deep health checks against the institutional gateway.
    """

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

    def validate_api_health(self) -> Dict[str, Any]:
        print("\n--- Runtime: API Gateway Health Probe ---")
        endpoints = ["/health", "/ready", "/api/v1/platform/status"]
        results = {"status": "PASS", "details": []}

        for endpoint in endpoints:
            url = f"{self.base_url}{endpoint}"
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"[OK] Endpoint {endpoint}: {response.status_code}")
                else:
                    results["status"] = "FAIL"
                    results["details"].append(f"UNHEALTHY_ENDPOINT: {endpoint} (Code: {response.status_code})")
                    print(f"[FAIL] Endpoint {endpoint}: {response.status_code}")
            except Exception as e:
                results["status"] = "FAIL"
                results["details"].append(f"CONNECTION_ERROR: {endpoint} ({str(e)})")
                print(f"[ERROR] Endpoint {endpoint}: Connection Failed")

        return results

    def validate_cognition_pipeline(self) -> Dict[str, Any]:
        """Validates that the cognition/query endpoint is responsive."""
        print("\n--- Runtime: Cognition Pipeline Smoke Test ---")
        url = f"{self.base_url}/api/v1/cognition/query"
        results = {"status": "PASS", "details": []}
        
        payload = {
            "prompt": "Institutional Health Status Check",
            "governance_level": "STANDARD"
        }
        
        try:
            # Note: This requires the Gemini CLI or its mock to be functional
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                print(f"[OK] Cognition Query: Pipeline Verified")
            else:
                results["status"] = "FAIL"
                results["details"].append(f"COGNITION_PIPELINE_ERROR: (Code: {response.status_code})")
                print(f"[FAIL] Cognition Query: {response.status_code}")
        except Exception as e:
            results["status"] = "FAIL"
            results["details"].append(f"COGNITION_CONNECTION_ERROR: {str(e)}")
            print(f"[ERROR] Cognition Query: Execution Failed")
            
        return results
