from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from orchestration.contracts.architecture_contract import DomainIdentity

class DomainState(BaseModel):
    domain: DomainIdentity
    status: str = "HEALTHY"
    last_event_id: Optional[str] = None
    active_contracts: List[str] = []
    metadata: Dict[str, Any] = {}

class PlatformStateRegistry(BaseModel):
    """
    Registry of the current state of all enterprise domains.
    Ensures state synchronization across the cognitive operating system.
    """
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    domain_states: Dict[DomainIdentity, DomainState] = {}

    def update_state(self, state: DomainState):
        self.domain_states[state.domain] = state

# Global State Registry
platform_state = PlatformStateRegistry()
