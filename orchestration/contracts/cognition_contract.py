from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from datetime import datetime
from orchestration.contracts.architecture_contract import DomainIdentity

class CognitionModality(str, Enum):
    GENERATIVE = "GENERATIVE"
    ANALYTICAL = "ANALYTICAL"
    PREDICTIVE = "PREDICTIVE"
    ADAPTIVE = "ADAPTIVE"
    REASONING = "REASONING"

class CognitionContract(BaseModel):
    """
    Enterprise Cognition Coordination Contract.
    Defines how AI agents and cognitive services interact.
    """
    model_config = ConfigDict(use_enum_values=True)
    
    cognition_id: str
    modality: CognitionModality
    target_domain: DomainIdentity
    
    # Cognitive input/output contracts
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    
    # Reasoning constraints
    max_tokens: int = 4096
    temperature_range: tuple = (0.0, 0.7)
    grounding_sources: List[str]
    
    # Governance & Safety
    safety_filters: List[str]
    audit_required: bool = True
    explainability_level: str = "HIGH"
    
    # Evolution controls
    supports_adaptive_evolution: bool = False
    governance_bypass_allowed: bool = False
