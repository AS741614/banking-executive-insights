import logging
import uuid
from datetime import datetime
from typing import Dict, Any

from ai.events.engines.event_bus import event_bus
from ai.events.models.event import CognitiveEvent, EventCategory, EventSeverity
from ai.events.contracts.event_types import CognitiveEventType
from ecos.governance.audit_logger import audit_logger

logger = logging.getLogger("esoteric_bank.ai.regulatory.workflows.kyc_lifecycle")

class KYCLifecycleOrchestrator:
    """
    Institutional Workflow Authority for KYC Customer Lifecycles.
    Orchestrates transitions between PENDING, EVALUATING, APPROVED, UNDER_REVIEW, and REJECTED states.
    
    Mandatory Rule: The orchestrator is the ONLY authority for lifecycle transitions.
    """

    def __init__(self):
        self._is_active = False

    async def start(self):
        """
        Registers institutional event subscribers for KYC lifecycle orchestration.
        """
        if self._is_active:
            return
        
        # Subscribe to KYC Evaluation completions
        event_bus.subscribe(EventCategory.COMPLIANCE, self.handle_evaluation_completed)
        self._is_active = True
        logger.info("KYC Lifecycle Orchestrator ACTIVATED.")

    async def handle_evaluation_completed(self, event: CognitiveEvent):
        """
        Reacts to KYC evaluation results and triggers institutional workflow transitions.
        """
        if event.action != CognitiveEventType.KYC_EVALUATION_COMPLETED:
            return

        payload = event.payload
        customer_id = payload.get("customer_id")
        compliance_status = payload.get("compliance_status")
        trace_id = event.trace_id

        logger.info(f"Orchestrating lifecycle for customer {customer_id} | Status: {compliance_status}")

        # 1. Update ECOS Institutional State Registry
        from ecos.main import ecos
        await ecos.state.set_state(
            domain="customer_lifecycle",
            key=customer_id,
            value=compliance_status,
            metadata={
                "trace_id": trace_id,
                "last_evaluation": event.event_id,
                "governance_tier": payload.get("governance_tier")
            }
        )

        # 2. Trigger Governance Reactivity (Conditional Regulatory Escalation)
        if compliance_status in ["REJECTED", "UNDER_REVIEW"]:
            await self._trigger_regulatory_escalation(event)

        # 3. Log Institutional Audit Entry
        await audit_logger.log_action(
            service_id="KYC_LIFECYCLE_ORCHESTRATOR",
            event_type="LIFECYCLE_TRANSITION",
            actor_identity="SYSTEM_ORCHESTRATOR",
            action_description=f"Customer {customer_id} transitioned to {compliance_status}",
            trace_id=trace_id,
            metadata={
                "customer_id": customer_id,
                "previous_state": "EVALUATING", # Simplified for Wave 2B
                "new_state": compliance_status
            }
        )

    async def _trigger_regulatory_escalation(self, event: CognitiveEvent):
        """
        Emits a REGULATORY_ESCALATION event into the institutional chain.
        """
        payload = event.payload
        customer_id = payload.get("customer_id")
        
        escalation_event = CognitiveEvent(
            event_id=str(uuid.uuid4()),
            trace_id=event.trace_id,
            timestamp=datetime.utcnow(),
            category=EventCategory.GOVERNANCE,
            severity=event.severity, # Inherit severity from evaluation
            source_component="KYCLifecycleOrchestrator",
            action=CognitiveEventType.REGULATORY_ESCALATION,
            payload={
                "domain": "REGULATORY_KYC",
                "customer_id": customer_id,
                "trigger": "COMPLIANCE_THRESHOLD_VIOLATION",
                "description": f"Mandatory escalation for {customer_id} due to {payload.get('compliance_status')} status.",
                "compliance_payload": payload
            }
        )
        
        await event_bus.publish(escalation_event)
        logger.warning(f"REGULATORY_ESCALATION triggered for customer {customer_id}")

# Singleton instance
kyc_orchestrator = KYCLifecycleOrchestrator()
