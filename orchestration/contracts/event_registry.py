from typing import Dict, Any, List, Type
from pydantic import BaseModel
from ai.events.models.event import EventCategory, EventSeverity

class EventContract(BaseModel):
    """
    Formal schema definition for a cross-domain event.
    """
    event_type: str
    category: EventCategory
    required_payload_keys: List[str]
    severity_mapping: Dict[str, EventSeverity]
    description: str

class EventContractRegistry:
    """
    Global registry for enterprise event contracts.
    Prevents ontology drift by enforcing schema consistency.
    """
    def __init__(self):
        self._contracts: Dict[str, EventContract] = {}

    def register_contract(self, contract: EventContract):
        self._contracts[contract.event_type] = contract

    def validate_event(self, event_type: str, payload: Dict[str, Any]) -> bool:
        if event_type not in self._contracts:
            return False
        
        contract = self._contracts[event_type]
        for key in contract.required_payload_keys:
            if key not in payload:
                return False
        return True

# Global registry instance
enterprise_event_registry = EventContractRegistry()

# Initialize with core platform events
enterprise_event_registry.register_contract(
    EventContract(
        event_type="LIQUIDITY_GOVERNANCE_DRIFT",
        category=EventCategory.GOVERNANCE,
        required_payload_keys=["region", "segment", "total_net_flow"],
        severity_mapping={"HIGH": EventSeverity.HIGH},
        description="Detected sustained liquidity deterioration."
    )
)
