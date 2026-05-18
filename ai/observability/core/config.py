import os
from pydantic_settings import BaseSettings
from typing import Dict

class ObservabilitySettings(BaseSettings):
    # Telemetry Baselines
    DRIFT_THRESHOLD: float = 0.25
    LATENCY_THRESHOLD_MS: float = 200.0
    HEALTH_CRITICAL_THRESHOLD: float = 0.4
    
    # Logging
    LOG_STRUCTURED: bool = True
    LOG_LEVEL: str = os.getenv("OBSERVABILITY_LOG_LEVEL", "INFO")
    
    # Trace Retention (Local)
    MAX_TRACES_IN_MEMORY: int = 1000
    
    # Institutional Baselines
    INSTITUTIONAL_BASELINES: Dict[str, float] = {
        "aml_severity_avg": 0.45,
        "kyc_approval_rate": 0.92,
        "fraud_false_positive_rate": 0.05,
        "cognition_latency_ms": 150.0,
        "governance_drift_index": 0.1
    }

obs_settings = ObservabilitySettings()
