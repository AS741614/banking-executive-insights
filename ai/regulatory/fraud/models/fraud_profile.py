from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict, confloat

class FraudType(str, Enum):
    IDENTITY_THEFT = "IDENTITY_THEFT"
    ACCOUNT_TAKEOVER = "ACCOUNT_TAKEOVER"
    PAYMENT_FRAUD = "PAYMENT_FRAUD"
    MULE_ACTIVITY = "MULE_ACTIVITY"
    SOCIAL_ENGINEERING = "SOCIAL_ENGINEERING"
    INTERNAL_FRAUD = "INTERNAL_FRAUD"
    SYNTHETIC_IDENTITY = "SYNTHETIC_IDENTITY"

class FraudSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class FraudGovernanceMetadata(BaseModel):
    model_config = ConfigDict(frozen=True)
    audit_id: str
    audit_timestamp: datetime = Field(default_factory=datetime.utcnow)
    governance_version: str = "v1.0.0"

class FraudPatternProfile(BaseModel):
    detected_patterns: List[str] = Field(default_factory=list)
    anomaly_score: confloat(ge=0.0, le=1.0) = 0.0
    velocity_variance: float = 0.0
    device_fingerprint_risk: confloat(ge=0.0, le=1.0) = 0.0
    geolocation_risk: confloat(ge=0.0, le=1.0) = 0.0

class FraudIntelligenceProfile(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    
    fraud_id: str
    customer_id: str
    transaction_id: Optional[str] = None
    
    fraud_type: FraudType
    severity: FraudSeverity
    confidence_score: confloat(ge=0.0, le=1.0)
    
    pattern_profile: FraudPatternProfile
    risk_indicators: List[str] = Field(default_factory=list)
    
    is_blocked: bool = False
    governance_escalation_required: bool = False
    
    audit: FraudGovernanceMetadata
