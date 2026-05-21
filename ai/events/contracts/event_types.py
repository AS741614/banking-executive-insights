from enum import Enum

class CognitiveEventType(str, Enum):
    """
    Centralized Institutional Event Types for the ESOTERIC platform.
    Ensures architectural consistency across cognition, governance, and regulatory layers.
    """
    
    # KYC & Regulatory Domain
    KYC_EVALUATION_COMPLETED = "KYC_EVALUATION_COMPLETED"
    REGULATORY_ESCALATION = "REGULATORY_ESCALATION"
    
    # Governance Domain
    GOVERNANCE_DRIFT_DETECTED = "GOVERNANCE_DRIFT_DETECTED"
    GOVERNANCE_ACTION_EXECUTED = "GOVERNANCE_ACTION_EXECUTED"
    
    # Audit Domain
    AUDIT_ENTRY_CREATED = "AUDIT_ENTRY_CREATED"
    
    # Platform Domain
    SYSTEM_HEALTH_SIGNAL = "SYSTEM_HEALTH_SIGNAL"
    COGNITIVE_TASK_DISPATCHED = "COGNITIVE_TASK_DISPATCHED"
