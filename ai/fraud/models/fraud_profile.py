from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict, confloat

class FraudRiskLevel(str, Enum):
    NEGLEGIBLE = "NEGLEGIBLE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class DeviceIntelligenceProfile(BaseModel):
    device_id: str
    ip_address: str
    vpn_detected: bool = False
    proxy_detected: bool = False
    tor_detected: bool = False
    emulator_detected: bool = False
    location_country: str
    velocity_count: int = 0
    risk_score: confloat(ge=0.0, le=1.0) = 0.0

class BehavioralAnomalyProfile(BaseModel):
    velocity_variance: float = 0.0
    geographical_drift: bool = False
    unusual_time_pattern: bool = False
    amount_variance: float = 0.0
    behavioral_risk_score: confloat(ge=0.0, le=1.0) = 0.0

class FraudIntelligenceProfile(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    
    fraud_assessment_id: str
    customer_id: str
    transaction_id: Optional[str] = None
    
    risk_level: FraudRiskLevel
    composite_fraud_score: confloat(ge=0.0, le=1.0)
    
    device_intelligence: DeviceIntelligenceProfile
    behavioral_anomaly: BehavioralAnomalyProfile
    
    detected_patterns: List[str] = Field(default_factory=list)
    is_synthetic_identity_suspected: bool = False
    account_takeover_probability: confloat(ge=0.0, le=1.0) = 0.0
    
    governance_action: str = "MONITOR"
    audit_timestamp: datetime = Field(default_factory=datetime.utcnow)
    governance_commentary: str
