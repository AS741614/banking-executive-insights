from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, ConfigDict

class EventSeverity(str, Enum):
    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class EventCategory(str, Enum):
    COGNITION = "COGNITION"
    GOVERNANCE = "GOVERNANCE"
    COMPLIANCE = "COMPLIANCE"
    OPERATIONAL = "OPERATIONAL"
    ADAPTIVE = "ADAPTIVE"

class CognitiveEvent(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    
    event_id: str
    trace_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    category: EventCategory
    severity: EventSeverity
    source_component: str
    action: str
    payload: Dict[str, Any]
    governance_context: Optional[Dict[str, Any]] = None

class EventCorrelationProfile(BaseModel):
    correlation_id: str
    related_event_ids: List[str]
    root_cause_inference: Optional[str] = None
    impact_level: EventSeverity
