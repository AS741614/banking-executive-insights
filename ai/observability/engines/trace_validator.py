import logging
from typing import List, Dict, Any
from ai.observability.models.telemetry import CognitionTrace

logger = logging.getLogger("esoteric_bank.observability.trace_validator")

class CognitionTraceValidator:
    """
    Institutional Cognition Trace Validator.
    Ensures that every distributed cognitive cycle follows governance standards.
    """

    @staticmethod
    def validate_trace_integrity(trace: CognitionTrace) -> bool:
        """
        Validates a trace for completeness and institutional consistency.
        """
        if not trace.trace_id or not trace.steps:
            logger.error(f"Trace {trace.trace_id} failed integrity check: Missing ID or steps.")
            return False
        
        # Check for mandatory governance steps
        has_inference = False
        has_validation = False
        
        for step in trace.steps:
            action = step.get("action", "").upper()
            if "INFERENCE" in action:
                has_inference = True
            if "VALIDATION" in action or "GOVERNANCE" in action:
                has_validation = True
        
        if not (has_inference and has_validation):
            logger.warning(f"Trace {trace.trace_id} lacks mandatory institutional reasoning steps.")
            return False
            
        return True

    @staticmethod
    def calculate_latency_compliance(trace: CognitionTrace, threshold_ms: float) -> bool:
        if not trace.duration_ms:
            return False
        return trace.duration_ms <= threshold_ms
