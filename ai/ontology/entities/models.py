from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

class EntityCategory(str, Enum):
    ACTOR = "ACTOR"          # Customers, Institutions, Agents
    ASSET = "ASSET"          # Accounts, Securities, Loans
    ACTION = "ACTION"        # Transactions, Audits, Trades
    CONCEPT = "CONCEPT"      # Risk, Compliance, Governance
    METRIC = "METRIC"        # KPI, Score, Limit

class InstitutionalEntity(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    entity_id: str = Field(..., description="Unique institutional semantic identifier")
    name: str
    category: EntityCategory
    description: str
    semantic_tags: List[str] = Field(default_factory=list)
    governance_clearance: str = "TIER_1"

class SemanticProperty(BaseModel):
    name: str
    data_type: str
    is_required: bool = False
    governance_rule: Optional[str] = None

class EntityDefinition(BaseModel):
    entity: InstitutionalEntity
    properties: List[SemanticProperty]
    version: str = "1.0.0"
