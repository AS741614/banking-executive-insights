from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, confloat

class TransactionLifecycleStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    HELD = "HELD"
    REJECTED = "REJECTED"
    REVERSED = "REVERSED"
    ESCALATED = "ESCALATED"

class AMLGovernanceMetadata(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    audit_id: str = Field(..., description="Unique enterprise audit identifier for the transaction assessment")
    audit_timestamp: datetime = Field(default_factory=datetime.utcnow)
    audit_source: str = Field(..., description="System or agent responsible for the cognitive evaluation")
    governance_version: str = Field("v1.0.0")

class JurisdictionExposureProfile(BaseModel):
    transaction_country: str = Field(..., min_length=2, max_length=3)
    destination_country: str = Field(..., min_length=2, max_length=3)
    cross_border_flag: bool = False
    high_risk_jurisdiction_flag: bool = False

class SuspiciousActivityProfile(BaseModel):
    suspicious_activity_flag: bool = False
    regulatory_watchlist_flag: bool = False
    crypto_transaction_flag: bool = False
    sar_filing_recommended: bool = False

class TransactionBehaviorProfile(BaseModel):
    velocity_score: confloat(ge=0.0, le=1.0) = 0.0
    structuring_score: confloat(ge=0.0, le=1.0) = 0.0
    layering_score: confloat(ge=0.0, le=1.0) = 0.0
    anomaly_score: confloat(ge=0.0, le=1.0) = 0.0
    cash_intensity_score: confloat(ge=0.0, le=1.0) = 0.0
    behavioral_risk_score: confloat(ge=0.0, le=1.0) = 0.0

class AMLRiskAssessment(BaseModel):
    aml_severity: confloat(ge=0.0, le=1.0) = 0.0
    governance_risk_score: confloat(ge=0.0, le=1.0) = 0.0
    governance_escalation_flag: bool = False
    requires_manual_review: bool = False

class AMLTransactionProfile(BaseModel):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)

    transaction_id: str = Field(..., description="Unique institutional transaction identifier")
    customer_id: str = Field(..., description="Associated customer identity reference")
    account_id: str = Field(..., description="Source or destination account reference")
    
    transaction_type: str = Field(..., description="Classification of transaction (e.g., WIRE, ACH, INTERNAL)")
    transaction_amount: float = Field(..., gt=0.0, description="Absolute transaction value")
    transaction_currency: str = Field(..., min_length=3, max_length=3)
    transaction_channel: str = Field(..., description="Origination channel (e.g., MOBILE, BRANCH, API)")
    counterparty_type: str = Field(..., description="Entity classification of the counterparty")
    transaction_timestamp: datetime

    jurisdiction_exposure: JurisdictionExposureProfile
    behavior_profile: TransactionBehaviorProfile
    suspicious_activity: SuspiciousActivityProfile
    risk_assessment: AMLRiskAssessment

    lifecycle_status: TransactionLifecycleStatus = Field(default=TransactionLifecycleStatus.PENDING)
    audit: AMLGovernanceMetadata
