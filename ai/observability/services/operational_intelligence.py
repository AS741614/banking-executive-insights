import logging
import uuid
from datetime import datetime
from typing import Dict, Any, List

from ai.observability.models.telemetry import GovernanceTelemetry, DriftReport
from ai.observability.engines.drift_detector import GovernanceDriftDetector
from ai.events.engines.event_bus import event_bus
from ai.events.models.event import CognitiveEvent, EventCategory, EventSeverity

logger = logging.getLogger("esoteric_bank.observability.operational_intelligence")

class OperationalIntelligenceService:
    """
    Enterprise Operational Intelligence Service.
    Orchestrates platform health monitoring and governance telemetry.
    """

    def __init__(self):
        self.drift_detector = GovernanceDriftDetector()

    async def generate_platform_telemetry(
        self, 
        component_id: str, 
        current_metrics: Dict[str, float]
    ) -> GovernanceTelemetry:
        """
        Generates a full governance telemetry profile for a platform component.
        """
        logger.info(f"Generating operational intelligence for component: {component_id}")

        # 1. Detect Drift
        drift_reports = self.drift_detector.analyze_drift(current_metrics)
        
        # 2. Compute Health and Risk
        anomalies = [r for r in drift_reports if r.is_anomaly]
        system_health = max(0.0, 1.0 - (len(anomalies) * 0.2))
        risk_exposure = min(1.0, len(anomalies) * 0.25)

        telemetry = GovernanceTelemetry(
            telemetry_id=f"TEL-{uuid.uuid4().hex[:8].upper()}",
            component_id=component_id,
            system_health=system_health,
            risk_exposure=risk_exposure,
            drift_reports=drift_reports,
            active_incidents=len(anomalies)
        )

        # 3. Publish Critical Events
        for report in anomalies:
            event = CognitiveEvent(
                event_id=f"EVT-{uuid.uuid4().hex[:8].upper()}",
                trace_id="OPERATIONAL_MONITOR",
                category=EventCategory.OPERATIONAL,
                severity=EventSeverity.HIGH,
                source_component=component_id,
                action="GOVERNANCE_DRIFT_DETECTED",
                payload={
                    "metric": report.metric_name,
                    "variance": report.variance,
                    "current": report.current_value
                }
            )
            await event_bus.publish(event)

        return telemetry
