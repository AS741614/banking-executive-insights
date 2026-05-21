import logging
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional

from app.schemas.governance import GovernanceState, RegulatoryEscalation, EscalationSeverity, EscalationStatus
from ai.events.engines.event_bus import event_bus as cognitive_event_bus
from ai.events.models.event import CognitiveEvent, EventCategory, EventSeverity
from ai.events.contracts.event_types import CognitiveEventType

logger = logging.getLogger("esoteric_bank.ai.governance.intelligence")

class GovernanceIntelligenceService:
    """
    Aggregates governance intelligence signals across institutional domains.
    Provides a unified interface for executive governance cognition.
    """
    
    def __init__(self):
        self._escalations: List[RegulatoryEscalation] = []
        self._is_active = False

    async def start(self):
        """
        Activates governance reactivity by subscribing to institutional signals.
        """
        if self._is_active:
            return
        
        # Subscribe to Regulatory Escalations from any source domain
        cognitive_event_bus.subscribe(EventCategory.GOVERNANCE, self.handle_governance_signal)
        self._is_active = True
        logger.info("Governance Intelligence Service REACTIVITY ACTIVATED.")

    async def handle_governance_signal(self, event: CognitiveEvent):
        """
        Reactively processes incoming governance signals (e.g., Escalations, Drift).
        """
        try:
            # Prevent infinite recursion from self-published events
            if event.source_component == "GovernanceIntelligenceService":
                return

            from ecos.main import ecos
            logger.info(f"handle_governance_signal RECEIVED event: {event.action} | Category: {event.category}")
            # Use .value for robust Enum value matching across Python versions
            if str(event.action) == str(CognitiveEventType.REGULATORY_ESCALATION.value):
                logger.info("MATCHED REGULATORY_ESCALATION. Registering...")
                payload = event.payload
                escalation = RegulatoryEscalation(
                    escalation_id=str(uuid.uuid4()),
                    timestamp=event.timestamp,
                    domain=payload.get("domain", "UNKNOWN"),
                    severity=EscalationSeverity(event.severity), # Safe cast since event.severity is already a string
                    trigger=payload.get("trigger", "MANUAL"),
                    description=payload.get("description", "No description"),
                    status=EscalationStatus.PENDING,
                    metadata={
                        "trace_id": event.trace_id,
                        "customer_id": payload.get("customer_id")
                    }
                )
                await self.register_escalation(escalation)
            
            elif str(event.action) == str(CognitiveEventType.GOVERNANCE_DRIFT_DETECTED.value):
                payload = event.payload
                logger.warning(f"GOVERNANCE_DRIFT captured from event bus for domain: {payload.get('domain')}")
                # Reflect drift in institutional state
                await ecos.state.set_state(
                    domain="governance",
                    key="drift_detected",
                    value=True,
                    metadata={
                        "variance": payload.get("drift_index"),
                        "domain": payload.get("domain"),
                        "trace_id": event.trace_id
                    }
                )
                await ecos.state.set_state(
                    domain="governance",
                    key="drift_index",
                    value=payload.get("drift_index"),
                    metadata={"updated_at": event.timestamp.isoformat()}
                )
        except Exception as e:
            logger.error(f"FATAL error in handle_governance_signal: {str(e)}", exc_info=True)
            raise

    async def get_governance_cognition(self) -> GovernanceState:
        """
        Retrieves the latest governance state aggregated from ECOS and AI drift detectors.
        """
        from ecos.main import ecos
        # Aggregate real-time signals from ECOS Institutional State Registry
        governance_states = await ecos.state.get_domain_state("governance")
        
        drift_detected = governance_states.get("drift_detected", False)
        drift_index = governance_states.get("drift_index", 0.0)
        
        # Determine status based on drift and escalations
        governance_status = "SYNCHRONIZED"
        if drift_detected or drift_index > 0.5:
            governance_status = "DEGRADED"
        
        critical_escalations = [e for e in self._escalations if e.severity == EscalationSeverity.CRITICAL and e.status == EscalationStatus.PENDING]
        if critical_escalations:
            governance_status = "CRITICAL"

        return GovernanceState(
            governance_status=governance_status,
            active_policies=int(governance_states.get("active_policy_count", 42)),
            compliance_score=float(governance_states.get("compliance_score", 98.4)),
            last_audit_timestamp=datetime.utcnow(),
            drift_detected=drift_detected or drift_index > 0.2,
            pending_escalations=len(self._escalations)
        )

    async def register_escalation(self, escalation: RegulatoryEscalation):
        """
        Registers a new regulatory escalation and propagates institutional events.
        """
        try:
            from ecos.main import ecos
            self._escalations.append(escalation)
            logger.info(f"Escalation REGISTERED. Total pending: {len(self._escalations)}")
            
            # Reflect in institutional state
            await ecos.state.set_state(
                domain="governance",
                key="escalation_count",
                value=len(self._escalations),
                metadata={"last_escalation": escalation.escalation_id}
            )
            
            await self._propagate_governance_event(
                action=CognitiveEventType.REGULATORY_ESCALATION.value,
                description=f"New escalation in {escalation.domain}: {escalation.description}",
                severity=escalation.severity,
                metadata=escalation.model_dump()
            )
        except Exception as e:
            logger.error(f"FATAL error in register_escalation: {str(e)}", exc_info=True)
            raise

    async def _propagate_governance_event(self, action: str, description: str, severity: str, metadata: Dict[str, Any]):
        """
        Ensures governance events are emitted into the institutional event chain.
        Emitting to cognitive_event_bus triggers ECOS state updates and SSE streaming.
        """
        trace_id = metadata.get("trace_id", str(uuid.uuid4()))
        
        # Severity Mapping
        severity_map = {
            EscalationSeverity.CRITICAL: EventSeverity.CRITICAL,
            EscalationSeverity.HIGH: EventSeverity.HIGH,
            EscalationSeverity.MEDIUM: EventSeverity.MEDIUM,
            EscalationSeverity.LOW: EventSeverity.LOW
        }
        
        cognitive_event = CognitiveEvent(
            event_id=str(uuid.uuid4()),
            trace_id=trace_id,
            timestamp=datetime.utcnow(),
            category=EventCategory.GOVERNANCE,
            severity=severity_map.get(severity, EventSeverity.INFO),
            source_component="GovernanceIntelligenceService",
            action=action,
            payload=metadata
        )
        
        # Publish to the cognitive event bus - this is the standard entry point for ECOS
        await cognitive_event_bus.publish(cognitive_event)
        
        logger.info(f"Governance event published to bus: {action} | Severity: {severity}")

# Singleton instance
governance_intelligence = GovernanceIntelligenceService()
