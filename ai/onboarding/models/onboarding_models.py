from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

class OnboardingType(str, Enum):
    NEW_DATA_SOURCE = "NEW_DATA_SOURCE"
    SCHEMA_EVOLUTION = "SCHEMA_EVOLUTION"
    KPI_ADAPTATION = "KPI_ADAPTATION"

class OnboardingStatus(str, Enum):
    SUBMITTED = "SUBMITTED"
    VALIDATING = "VALIDATING"
    GOVERNANCE_REVIEW = "GOVERNANCE_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    SYNCING = "SYNCING"
    COMPLETED = "COMPLETED"

class SchemaField(BaseModel):
    name: str
    data_type: str
    description: str
    is_pii: bool = False
    governance_tag: Optional[str] = None

class DataOnboardingRequest(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    
    request_id: str
    onboarding_type: OnboardingType
    source_name: str
    description: str
    
    proposed_schema: List[SchemaField]
    context_metadata: Dict[str, Any] = Field(default_factory=dict)
    
    status: OnboardingStatus = OnboardingStatus.SUBMITTED
    created_at: datetime = Field(default_factory=datetime.utcnow)
    trace_id: str

class KPIAdaptationProfile(BaseModel):
    kpi_name: str
    source_metric: str
    calculation_logic: str
    semantic_category: str
    governance_thresholds: Dict[str, float]
    impact_analysis: str
