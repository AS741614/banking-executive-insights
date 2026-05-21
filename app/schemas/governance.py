from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum

class EscalationSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class EscalationStatus(str, Enum):
    PENDING = "PENDING"
    REVIEW = "REVIEW"
    RESOLVED = "RESOLVED"
    DISMISSED = "DISMISSED"

class RegulatoryEscalation(BaseModel):
    escalation_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    domain: str
    severity: EscalationSeverity
    trigger: str
    description: str
    status: EscalationStatus
    metadata: Dict[str, Any] = Field(default_factory=dict)

class GovernanceActionType(str, Enum):
    POLICY_UPDATE = "POLICY_UPDATE"
    RESTRICTION_APPLIED = "RESTRICTION_APPLIED"
    REALIGNMENT_TRIGGERED = "REALIGNMENT_TRIGGERED"
    ACCESS_REVOKED = "ACCESS_REVOKED"

class GovernanceAction(BaseModel):
    action_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    action_type: GovernanceActionType
    actor: str
    target_domain: str
    description: str
    impact_level: str
    governance_signature: str

class AuditEntry(BaseModel):
    entry_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    service_id: str
    event_type: str
    actor_identity: str
    action_description: str
    status: str
    trace_id: Optional[str] = None
    integrity_checksum: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class GovernanceState(BaseModel):
    governance_status: str
    active_policies: int
    compliance_score: float
    last_audit_timestamp: datetime
    drift_detected: bool
    pending_escalations: int
