from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

class RecommendationType(str, Enum):
    SCHEMA_EVOLUTION = "SCHEMA_EVOLUTION"
    ONTOLOGY_EXPANSION = "ONTOLOGY_EXPANSION"
    KPI_DISCOVERY = "KPI_DISCOVERY"
    GOVERNANCE_ADAPTATION = "GOVERNANCE_ADAPTATION"
    COGNITIVE_DRIFT_CORRECTION = "COGNITIVE_DRIFT_CORRECTION"

class EvolutionSeverity(str, Enum):
    MINOR = "MINOR"
    MAJOR = "MAJOR"
    CRITICAL = "CRITICAL"
    BREAKING = "BREAKING"

class SemanticInference(BaseModel):
    field_name: str
    inferred_type: str
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    suggested_ontology_mapping: Optional[str] = None
    reasoning: str

class AdaptiveRecommendation(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    
    recommendation_id: str
    type: RecommendationType
    severity: EvolutionSeverity
    summary: str
    detailed_plan: Dict[str, Any]
    impact_analysis: str
    
    inferences: List[SemanticInference] = Field(default_factory=list)
    
    requires_approval: bool = True
    approval_status: str = "PENDING"
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    governance_metadata: Dict[str, Any] = Field(default_factory=dict)

class OntologyNode(BaseModel):
    name: str
    description: str
    attributes: List[str]
    relationships: List[Dict[str, str]] # e.g., [{"type": "belongs_to", "target": "Customer"}]
