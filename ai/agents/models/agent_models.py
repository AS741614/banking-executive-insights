from enum import Enum
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class AgentType(str, Enum):
    REGULATORY = "REGULATORY"
    FRAUD = "FRAUD"
    TREASURY = "TREASURY"
    GOVERNANCE = "GOVERNANCE"
    EXECUTIVE = "EXECUTIVE"
    ORCHESTRATOR = "ORCHESTRATOR"

class AgentStatus(str, Enum):
    IDLE = "IDLE"
    BUSY = "BUSY"
    OFFLINE = "OFFLINE"
    ERROR = "ERROR"

class CognitiveMessage(BaseModel):
    message_id: str
    sender_id: str
    receiver_id: Optional[str] = None # None for broadcast
    correlation_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    intent: str
    content: Dict[str, Any]
    ontology_references: List[str] = Field(default_factory=list)
    governance_clearance: str = "TIER_1"

class CognitiveTask(BaseModel):
    task_id: str
    requester_id: str
    assigned_agent_id: Optional[str] = None
    priority: int = 1
    description: str
    context: Dict[str, Any] = Field(default_factory=dict)
    deadline: Optional[datetime] = None
    status: str = "PENDING"
