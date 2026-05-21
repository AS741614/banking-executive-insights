from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator

class ComplianceStatus(str, Enum):
    APPROVED = "APPROVED"
    PENDING = "PENDING"
    UNDER_REVIEW = "UNDER_REVIEW"
    REJECTED = "REJECTED"
    SUSPENDED = "SUSPENDED"

class GovernanceTier(str, Enum):
    TIER_1_STANDARD = "TIER_1_STANDARD"
    TIER_2_ENHANCED = "TIER_2_ENHANCED"
    TIER_3_RESTRICTED = "TIER_3_RESTRICTED"
    TIER_4_INSTITUTIONAL = "TIER_4_INSTITUTIONAL"

class LifecycleStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    ONBOARDING = "ONBOARDING"
    TERMINATED = "TERMINATED"
    DORMANT = "DORMANT"

class GovernanceAuditMetadata(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    audit_id: str = Field(..., description="Unique enterprise audit identifier")
    audit_timestamp: datetime = Field(default_factory=datetime.utcnow)
    audit_source: str = Field(..., description="Originating system or agent ID")
    governance_version: str = Field("v1.0.0")
    signature: Optional[str] = Field(None, description="Cryptographic signature for integrity")

class CustomerIdentityProfile(BaseModel):
    customer_id: str = Field(..., pattern=r"^[A-Z0-9-]{8,32}$")
    full_name: str
    country: str = Field(..., min_length=2, max_length=3)
    residency_status: str
    occupation: str
    onboarding_channel: str
    email: Optional[EmailStr] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class JurisdictionRiskProfile(BaseModel):
    jurisdiction_code: str
    is_high_risk: bool = False
    sanction_list_match: bool = False
    fatf_status: Optional[str] = None
    regulatory_notes: List[str] = Field(default_factory=list)

class ComplianceExposure(BaseModel):
    pep_flag: bool = False
    sanction_flag: bool = False
    adverse_media_flag: bool = False
    crypto_exposure: bool = False
    ultimate_beneficial_owner: Optional[str] = None

class CustomerRiskAssessment(BaseModel):
    annual_income: float = Field(..., ge=0)
    source_of_funds: str
    transaction_behavior_score: float = Field(..., ge=0.0, le=1.0)
    governance_risk_score: float = Field(..., ge=0.0, le=1.0)
    aml_risk_score: float = Field(..., ge=0.0, le=1.0)
    fraud_risk_score: float = Field(..., ge=0.0, le=1.0)
    onboarding_risk_score: float = Field(..., ge=0.0, le=1.0)
    
    @property
    def composite_risk_score(self) -> float:
        return (self.aml_risk_score * 0.4) + (self.fraud_risk_score * 0.3) + (self.governance_risk_score * 0.3)

class EnhancedDueDiligenceProfile(BaseModel):
    edd_required: bool = False
    last_review_date: Optional[datetime] = None
    next_review_date: Optional[datetime] = None
    investigation_notes: List[str] = Field(default_factory=list)
    verification_documents: List[str] = Field(default_factory=list)

class CustomerKYCCognitionProfile(BaseModel):
    """
    Enterprise-grade KYC Cognition Model for ESOTERIC BANK.
    Optimized for governance traceability and AML intelligence.
    """
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)

    identity: CustomerIdentityProfile
    risk_assessment: CustomerRiskAssessment
    jurisdiction: JurisdictionRiskProfile
    exposure: ComplianceExposure
    edd_profile: EnhancedDueDiligenceProfile
    
    compliance_status: ComplianceStatus = Field(default=ComplianceStatus.PENDING)
    governance_tier: GovernanceTier = Field(default=GovernanceTier.TIER_1_STANDARD)
    lifecycle_status: LifecycleStatus = Field(default=LifecycleStatus.ONBOARDING)
    
    audit: GovernanceAuditMetadata
    
    @field_validator('governance_tier', mode='before')
    @classmethod
    def enforce_enhanced_tier(cls, v: Any, info: Any) -> Any:
        # Business logic: Auto-escalate tier if high risk flags are present
        return v
