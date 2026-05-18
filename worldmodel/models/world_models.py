from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

class InstitutionalEntityType(str, Enum):
    ORGANIZATION_UNIT = "ORGANIZATION_UNIT"
    BUSINESS_PROCESS = "BUSINESS_PROCESS"
    REGULATORY_FRAMEWORK = "REGULATORY_FRAMEWORK"
    GOVERNANCE_COMMITTEE = "GOVERNANCE_COMMITTEE"
    SYSTEM_COMPONENT = "SYSTEM_COMPONENT"
    GEOGRAPHIC_REGION = "GEOGRAPHIC_REGION"

class OperationalRelationshipType(str, Enum):
    REPORTS_TO = "REPORTS_TO"
    GOVERNS = "GOVERNS"
    DEPENDS_ON = "DEPENDS_ON"
    OPERATES_IN = "OPERATES_IN"
    IMPLEMENTS = "IMPLEMENTS"
    MONITORS = "MONITORS"

class InstitutionalEntity(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    entity_id: str = Field(..., description="Unique institutional identifier")
    name: str
    entity_type: InstitutionalEntityType
    description: str
    governance_clearance: str = "TIER_1"
    metadata: Dict[str, Any] = Field(default_factory=dict)

class OperationalRelationship(BaseModel):
    source_id: str
    relationship_type: OperationalRelationshipType
    target_id: str
    confidence_score: float = Field(1.0, ge=0.0, le=1.0)
    effective_from: datetime = Field(default_factory=datetime.utcnow)
    effective_to: Optional[datetime] = None

class TemporalState(BaseModel):
    entity_id: str
    attribute_name: str
    value: Any
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    trace_id: str

class SituationalAwarenessReport(BaseModel):
    report_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    summary: str
    active_critical_risks: List[str]
    operational_continuity_score: float = Field(..., ge=0.0, le=1.0)
    governance_drift_index: float = Field(..., ge=0.0, le=1.0)
