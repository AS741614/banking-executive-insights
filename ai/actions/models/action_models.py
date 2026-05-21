from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

class ActionCategory(str, Enum):
    REMEDIATION = "REMEDIATION"      # Fixing a risk/issue
    OPTIMIZATION = "OPTIMIZATION"    # Improving treasury/ops
    REGULATORY = "REGULATORY"        # Compliance-mandated action
    OPERATIONAL = "OPERATIONAL"      # Standard maintenance

class ActionStatus(str, Enum):
    PROPOSED = "PROPOSED"
    PENDING_APPROVAL = "PENDING_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    EXECUTING = "EXECUTING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class ApprovalTier(str, Enum):
    TIER_1_STANDARD = "TIER_1_STANDARD"
    TIER_2_SENIOR = "TIER_2_SENIOR"
    TIER_3_EXECUTIVE = "TIER_3_EXECUTIVE"
    TIER_4_BOARD = "TIER_4_BOARD"

class InstitutionalAction(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    
    action_id: str
    category: ActionCategory
    title: str
    description: str
    remediation_reasoning: str
    
    impact_analysis: Dict[str, Any]
    required_approval_tier: ApprovalTier
    
    status: ActionStatus = ActionStatus.PROPOSED
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None
    
    trace_id: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class GovernanceWorkflow(BaseModel):
    workflow_id: str
    name: str
    description: str
    actions: List[InstitutionalAction]
    overall_status: ActionStatus = ActionStatus.PENDING_APPROVAL
    audit_log: List[Dict[str, Any]] = Field(default_factory=list)
