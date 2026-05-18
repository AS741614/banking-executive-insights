import requests
import streamlit as st
import logging
import os
from typing import Dict, Any, Optional

# Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000/api/v1")
TIMEOUT = 2

logger = logging.getLogger("ui.api_client")

class APIClient:
    @staticmethod
    def get_platform_status() -> Dict[str, Any]:
        """ Fetches the platform health status. """
        try:
            response = requests.get(f"{API_URL}/platform/status", timeout=TIMEOUT)
            response.raise_for_status()
            return response.json().get("data", {})
        except Exception as e:
            logger.error(f"Failed to fetch platform status: {e}")
            return {"status": "OFFLINE", "uptime": "N/A", "error": str(e)}

    @staticmethod
    def get_executive_summary() -> Optional[str]:
        """ Fetches the latest executive summary. """
        try:
            # Note: Checking both possible locations based on router config
            response = requests.get(f"{API_URL}/executive-intelligence", timeout=TIMEOUT)
            if response.status_code == 404:
                 # Fallback to direct file read if API is not fully mapped
                 return None
            response.raise_for_status()
            return response.json().get("content")
        except Exception as e:
            logger.error(f"Failed to fetch executive summary: {e}")
            return None

    @staticmethod
    def get_event_stream() -> list:
        """ Fetches the latest cognitive events. """
        try:
            response = requests.get(f"{API_URL}/cognition/events", timeout=TIMEOUT)
            response.raise_for_status()
            return response.json().get("data", {}).get("events", [])
        except Exception as e:
            logger.error(f"Failed to fetch event stream: {e}")
            return []

    @staticmethod
    def check_connectivity() -> bool:
        """ Checks if the API is reachable. """
        try:
            response = requests.get(f"{API_URL.replace('/api/v1', '')}/health", timeout=1)
            return response.status_code == 200
        except Exception:
            return False
