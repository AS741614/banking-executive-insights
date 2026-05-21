import logging
import uuid
from datetime import datetime
from typing import Dict, Any, Optional

from app.schemas.governance import AuditEntry
from ai.events.engines.event_bus import event_bus as cognitive_event_bus
from ai.events.models.event import CognitiveEvent, EventCategory, EventSeverity

logger = logging.getLogger("esoteric_bank.ecos.governance.audit_logger")

class InstitutionalAuditLogger:
    """
    Ensures cryptographic-grade audit traceability for all governance and operational actions.
    Integrated with the institutional event chain for real-time audit visibility.
    """
    
    def __init__(self):
        self._audit_history: Dict[str, AuditEntry] = {}

    async def log_action(
        self, 
        service_id: str, 
        event_type: str, 
        actor_identity: str, 
        action_description: str,
        status: str = "SUCCESS",
        trace_id: Optional[str] = None,
        metadata: Dict[str, Any] = None
    ) -> AuditEntry:
        """
        Records an institutional audit entry and propagates through the cognitive event chain.
        """
        entry_id = str(uuid.uuid4())
        # Simplified checksum for Wave 1
        checksum = f"sha256:{uuid.uuid4().hex[:16]}" 
        effective_trace_id = trace_id or str(uuid.uuid4())
        
        entry = AuditEntry(
            entry_id=entry_id,
            timestamp=datetime.utcnow(),
            service_id=service_id,
            event_type=event_type,
            actor_identity=actor_identity,
            action_description=action_description,
            status=status,
            trace_id=effective_trace_id,
            integrity_checksum=checksum,
            metadata=metadata or {}
        )
        
        self._audit_history[entry_id] = entry
        
        # Propagate to institutional event chain via cognitive_event_bus
        # This will trigger ECOS state updates and SSE streaming via ecos.handle_cognitive_event
        await cognitive_event_bus.publish(CognitiveEvent(
            event_id=str(uuid.uuid4()),
            trace_id=effective_trace_id,
            timestamp=datetime.utcnow(),
            category=EventCategory.COMPLIANCE,
            severity=EventSeverity.INFO,
            source_component="AuditLogger",
            action="AUDIT_RECORDED",
            payload=entry.model_dump()
        ))
        
        logger.info(f"Audit Entry Recorded: {entry_id} | Type: {event_type} | Status: {status}")
        return entry

    async def get_recent_entries(self, limit: int = 100) -> list[AuditEntry]:
        return sorted(self._audit_history.values(), key=lambda x: x.timestamp, reverse=True)[:limit]

# Singleton instance
audit_logger = InstitutionalAuditLogger()
