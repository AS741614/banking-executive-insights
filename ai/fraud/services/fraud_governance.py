import logging
import uuid
from typing import Dict, Any
from ai.fraud.engines.fraud_engine import FraudDetectionEngine
from ai.fraud.models.fraud_profile import FraudIntelligenceProfile, FraudRiskLevel
from ai.events.engines.event_bus import event_bus
from ai.events.models.event import CognitiveEvent, EventCategory, EventSeverity

logger = logging.getLogger("esoteric_bank.fraud.governance_service")

class FraudGovernanceService:
    """
    Enterprise Fraud Governance Service.
    Orchestrates fraud cognition and publishes institutional threat intelligence.
    """

    def __init__(self):
        self.detection_engine = FraudDetectionEngine()

    async def evaluate_transaction_fraud(
        self, 
        customer_id: str, 
        transaction_data: Dict[str, Any],
        historical_context: Dict[str, Any]
    ) -> FraudIntelligenceProfile:
        """
        Evaluates a transaction for fraud and publishes event intelligence.
        """
        logger.info(f"Orchestrating fraud governance for customer: {customer_id}")

        # 1. Execute Cognition
        profile = await self.detection_engine.execute_fraud_cognition(
            customer_id, 
            transaction_data, 
            historical_context
        )

        # 2. Map Severity for Eventing
        severity_map = {
            FraudRiskLevel.CRITICAL: EventSeverity.CRITICAL,
            FraudRiskLevel.HIGH: EventSeverity.HIGH,
            FraudRiskLevel.MEDIUM: EventSeverity.MEDIUM,
            FraudRiskLevel.LOW: EventSeverity.LOW,
            FraudRiskLevel.NEGLEGIBLE: EventSeverity.INFO
        }

        # 3. Publish Event Intelligence
        event = CognitiveEvent(
            event_id=f"EVT-FRAUD-{uuid.uuid4().hex[:8].upper()}",
            trace_id=transaction_data.get("trace_id", "FRAUD_MONITOR"),
            category=EventCategory.OPERATIONAL,
            severity=severity_map.get(profile.risk_level, EventSeverity.INFO),
            source_component="FraudGovernanceService",
            action="FRAUD_ASSESSMENT_COMPLETE",
            payload={
                "customer_id": customer_id,
                "fraud_score": profile.composite_fraud_score,
                "risk_level": profile.risk_level,
                "action": profile.governance_action,
                "patterns": profile.detected_patterns
            },
            governance_context={
                "ato_probability": profile.account_takeover_probability,
                "synthetic_identity_suspected": profile.is_synthetic_identity_suspected
            }
        )
        
        await event_bus.publish(event)

        return profile
