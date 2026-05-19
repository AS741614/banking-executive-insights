import requests
import streamlit as st
import logging
import os
from typing import Dict, Any, Optional, List

# Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000/api/v1")
TIMEOUT = 3

logger = logging.getLogger("ui.api_client")

class APIClient:
    @staticmethod
    def get_platform_status() -> Dict[str, Any]:
        """ Fetches the platform health snapshot. """
        try:
            response = requests.get(f"{API_URL}/platform/status", timeout=TIMEOUT)
            response.raise_for_status()
            return response.json().get("data", {})
        except Exception as e:
            logger.error(f"Failed to fetch platform status: {e}")
            return {"status": "OFFLINE", "uptime": "N/A", "error": str(e)}

    @staticmethod
    def get_executive_intelligence() -> Dict[str, Any]:
        """ Fetches the latest executive intelligence. """
        try:
            response = requests.get(f"{API_URL}/executive/intelligence", timeout=TIMEOUT)
            response.raise_for_status()
            return response.json().get("data", {})
        except Exception as e:
            logger.error(f"Failed to fetch executive intelligence: {e}")
            return {}

    @staticmethod
    def get_risk_intelligence() -> Dict[str, Any]:
        """ Fetches the latest risk intelligence. """
        try:
            response = requests.get(f"{API_URL}/risk/intelligence", timeout=TIMEOUT)
            response.raise_for_status()
            return response.json().get("data", {})
        except Exception as e:
            logger.error(f"Failed to fetch risk intelligence: {e}")
            return {}

    @staticmethod
    def get_governance_cognition() -> Dict[str, Any]:
        """ Fetches governance cognition data. """
        try:
            response = requests.get(f"{API_URL}/governance/cognition", timeout=TIMEOUT)
            response.raise_for_status()
            return response.json().get("data", {})
        except Exception as e:
            logger.error(f"Failed to fetch governance cognition: {e}")
            return {}

    @staticmethod
    def get_event_history() -> List[Dict[str, Any]]:
        """ Fetches the latest institutional event history. """
        try:
            response = requests.get(f"{API_URL}/platform/history", timeout=TIMEOUT)
            response.raise_for_status()
            return response.json().get("data", {}).get("events", [])
        except Exception as e:
            logger.error(f"Failed to fetch event history: {e}")
            return []

    @staticmethod
    def get_agents_distributed() -> Dict[str, Any]:
        """ Fetches distributed agents status. """
        try:
            response = requests.get(f"{API_URL}/agents/distributed", timeout=TIMEOUT)
            response.raise_for_status()
            return response.json().get("data", {})
        except Exception as e:
            logger.error(f"Failed to fetch agents status: {e}")
            return {}

    @staticmethod
    def get_regulatory_status() -> Dict[str, Any]:
        """ Fetches regulatory escalations and status. """
        try:
            response = requests.get(f"{API_URL}/regulatory/escalations/pending", timeout=TIMEOUT)
            response.raise_for_status()
            return response.json().get("data", {})
        except Exception as e:
            logger.error(f"Failed to fetch regulatory status: {e}")
            return {"pending_count": 0, "escalations": []}

    @staticmethod
    def check_connectivity() -> bool:
        """ Checks if the API is reachable. """
        try:
            response = requests.get(f"{API_URL}/platform/health", timeout=1)
            return response.status_code == 200
        except Exception:
            return False

    @staticmethod
    def query_cognition(query: str) -> Dict[str, Any]:
        """ Executes a dynamic cognitive query. """
        try:
            payload = {"query": query, "context_override": {}}
            response = requests.post(f"{API_URL}/cognition/query", json=payload, timeout=10)
            response.raise_for_status()
            return response.json().get("data", {})
        except Exception as e:
            logger.error(f"Failed to query cognition: {e}")
            return {"answer": f"Cognitive bridge failure: {str(e)}", "confidence": 0}
