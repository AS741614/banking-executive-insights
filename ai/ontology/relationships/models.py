from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class RelationshipType(str, Enum):
    OWNS = "OWNS"
    CONTROLLED_BY = "CONTROLLED_BY"
    ASSOCIATED_WITH = "ASSOCIATED_WITH"
    DERIVED_FROM = "DERIVED_FROM"
    PART_OF = "PART_OF"
    EXECUTES = "EXECUTES"

class SemanticRelationship(BaseModel):
    subject_id: str = Field(..., description="The source entity ID")
    predicate: RelationshipType
    object_id: str = Field(..., description="The target entity ID")
    confidence_score: float = Field(1.0, ge=0.0, le=1.0)
    governance_context: Optional[str] = None
    audit_trace_id: Optional[str] = None
