import logging
from datetime import datetime
from typing import Dict, List, Optional
from ai.observability.models.telemetry import CognitionTrace

logger = logging.getLogger("esoteric_bank.observability.trace_engine")

class DistributedTraceEngine:
    """
    Enterprise Distributed Cognition Trace Engine.
    Captures and correlates multi-agent reasoning steps across the platform.
    """

    def __init__(self):
        self._traces: Dict[str, CognitionTrace] = {}

    def start_trace(self, trace_id: str) -> CognitionTrace:
        if trace_id in self._traces:
            return self._traces[trace_id]
            
        trace = CognitionTrace(
            trace_id=trace_id,
            start_time=datetime.utcnow(),
            status="RUNNING"
        )
        self._traces[trace_id] = trace
        logger.info(f"Started Distributed Trace: {trace_id}")
        return trace

    def record_step(self, trace_id: str, action: str, agent_id: str, details: Dict[str, Any]):
        """Records a specific cognitive step within a trace."""
        if trace_id not in self._traces:
            self.start_trace(trace_id)
            
        step = {
            "timestamp": datetime.utcnow().isoformat(),
            "agent_id": agent_id,
            "action": action,
            "details": details
        }
        self._traces[trace_id].steps.append(step)
        logger.debug(f"Recorded step in trace {trace_id}: {action} by {agent_id}")

    def complete_trace(self, trace_id: str, status: str = "COMPLETED"):
        if trace_id in self._traces:
            trace = self._traces[trace_id]
            trace.end_time = datetime.utcnow()
            trace.duration_ms = (trace.end_time - trace.start_time).total_seconds() * 1000
            trace.status = status
            logger.info(f"Trace {trace_id} {status} in {trace.duration_ms:.2f}ms")

    def get_trace(self, trace_id: str) -> Optional[CognitionTrace]:
        return self._traces.get(trace_id)

from typing import Any
