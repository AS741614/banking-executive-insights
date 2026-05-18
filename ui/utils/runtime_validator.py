import sys
import os
import requests
import streamlit as st
import pkg_resources

def validate_environment():
    """
    Validates the local runtime environment for Streamlit execution.
    """
    required_packages = [
        "streamlit",
        "pandas",
        "plotly",
        "requests",
        "numpy"
    ]
    
    missing = []
    for pkg in required_packages:
        try:
            pkg_resources.get_distribution(pkg)
        except pkg_resources.DistributionNotFound:
            missing.append(pkg)
            
    if missing:
        return False, f"Missing required packages: {', '.join(missing)}"
    
    return True, "Environment validated."

def validate_api_connectivity(api_url: str):
    """
    Validates connectivity to the ESOTERIC Backend API.
    """
    try:
        # Check root health endpoint
        health_url = api_url.replace("/api/v1", "/health")
        response = requests.get(health_url, timeout=2)
        if response.status_code == 200:
            return True, "API is reachable and healthy."
        else:
            return False, f"API returned status code: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return False, f"API connectivity failed: {str(e)}"

def run_preflight_checks():
    """
    Runs all pre-flight checks before launching the UI.
    """
    print("--- ESOTERIC UI PRE-FLIGHT CHECKS ---")
    
    env_ok, env_msg = validate_environment()
    print(f"[ENV] {env_msg}")
    
    api_url = os.getenv("API_URL", "http://localhost:8000/api/v1")
    api_ok, api_msg = validate_api_connectivity(api_url)
    print(f"[API] {api_msg}")
    
    if not env_ok:
        print("CRITICAL: Environment validation failed. Please run 'pip install -r requirements.txt'")
        sys.exit(1)
        
    if not api_ok:
        print("WARNING: API is offline. Dashboard will run in DEGRADED mode.")
        
    print("--- PRE-FLIGHT CHECKS COMPLETE ---\n")

if __name__ == "__main__":
    run_preflight_checks()
