from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

class CognitiveServiceStatus(str, Enum):
    ONLINE = "ONLINE"
    DEGRADED = "DEGRADED"
    OFFLINE = "OFFLINE"
    MAINTENANCE = "MAINTENANCE"

class CognitiveTaskPriority(str, Enum):
    CRITICAL = "CRITICAL" # Executive-level, real-time
    HIGH = "HIGH"         # Compliance/Fraud alerts
    NORMAL = "NORMAL"     # Standard analytics
    LOW = "LOW"           # Background indexing/archiving

class CognitiveService(BaseModel):
    service_id: str
    name: str
    version: str
    status: CognitiveServiceStatus
    endpoints: Dict[str, str]
    capabilities: List[str]
    last_heartbeat: datetime = Field(default_factory=datetime.utcnow)

class CognitiveOrigin(str, Enum):
    PRODUCTION = "PRODUCTION"   # Certified institutional data
    SIMULATION = "SIMULATION"   # Synthetic crisis/test data
    REPLAY = "REPLAY"           # Historical crisis analysis

class CognitiveTask(BaseModel):
    task_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    priority: CognitiveTaskPriority
    origin: CognitiveOrigin = CognitiveOrigin.PRODUCTION
    service_domain: str
    action: str
    payload: Dict[str, Any]
    correlation_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None

class InstitutionalState(BaseModel):
    state_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    origin: CognitiveOrigin = CognitiveOrigin.PRODUCTION
    domain: str
    key: str
    value: Any
    metadata: Dict[str, Any] = Field(default_factory=dict)

class CognitiveTopology(BaseModel):
    topology_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    version: int
    services: List[CognitiveService]
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class OrchestrationEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    source: str
    event_type: str
    description: str
    severity: str # INFO, WARNING, ERROR, CRITICAL
    metadata: Dict[str, Any] = Field(default_factory=dict)
