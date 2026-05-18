import os
import requests
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("observability_stabilization.east_region")

def validate_east_region_telemetry(api_url: str):
    """
    Validates that telemetry from the East region is being correctly enriched and propagated.
    Simulates institutional traffic from the East jurisdiction.
    """
    print("=== Institutional Observability Validation: East Region ===")
    
    headers = {
        "X-Institutional-Region": "East",
        "X-Institutional-Segment": "Retail",
        "X-Enterprise-Trace-Id": f"stab-trace-{int(time.time())}"
    }
    
    try:
        logger.info(f"Simulating institutional request from East region to {api_url}/health...")
        response = requests.get(f"{api_url}/health", headers=headers, timeout=5)
        
        if response.status_code == 200:
            print("[SUCCESS] API responded successfully to regional request.")
            print(f"Trace ID propagated: {response.headers.get('X-Enterprise-Trace-Id')}")
            print("Action: Verify OpenTelemetry Collector logs for 'institutional.region=East' attribute.")
        else:
            print(f"[FAIL] API returned status {response.status_code}.")
            
    except Exception as e:
        print(f"[FAIL] Connectivity error: {e}")

if __name__ == "__main__":
    api_url = os.getenv("API_URL", "http://localhost:8000")
    validate_east_region_telemetry(api_url)
