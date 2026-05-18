import logging
from typing import Dict, Any, Optional, List
from threading import Lock
from datetime import datetime
from ecos.contracts.base import InstitutionalState, OrchestrationEvent

logger = logging.getLogger("ecos.state.registry")

class InstitutionalStateRegistry:
    """
    Centralized registry for managing the global state of the ESOTERIC Cognitive OS.
    Ensures thread-safe access to institutional awareness.
    """
    
    def __init__(self):
        self._state_store: Dict[str, Dict[str, InstitutionalState]] = {}
        self._lock = Lock()
        self._history: List[OrchestrationEvent] = []

    def set_state(self, domain: str, key: str, value: Any, metadata: Dict[str, Any] = None) -> InstitutionalState:
        """
        Updates or creates a state entry within a specific domain.
        """
        with self._lock:
            if domain not in self._state_store:
                self._state_store[domain] = {}
            
            state = InstitutionalState(
                domain=domain,
                key=key,
                value=value,
                metadata=metadata or {}
            )
            self._state_store[domain][key] = state
            
            # Log state change as an event
            event = OrchestrationEvent(
                source="StateRegistry",
                event_type="STATE_UPDATE",
                description=f"State updated: {domain}.{key}",
                severity="INFO",
                metadata={"domain": domain, "key": key}
            )
            self._history.append(event)
            
            logger.debug(f"State set: {domain}.{key}")
            return state

    def get_state(self, domain: str, key: str) -> Optional[InstitutionalState]:
        """
        Retrieves a state entry.
        """
        with self._lock:
            return self._state_store.get(domain, {}).get(key)

    def get_domain_state(self, domain: str) -> Dict[str, Any]:
        """
        Retrieves all state entries for a specific domain.
        """
        with self._lock:
            domain_data = self._state_store.get(domain, {})
            return {k: v.value for k, v in domain_data.items()}

    def flush_stale_states(self, ttl_seconds: int):
        """
        Removes states that haven't been updated within the TTL.
        """
        now = datetime.utcnow()
        with self._lock:
            for domain in list(self._state_store.keys()):
                for key in list(self._state_store[domain].keys()):
                    state = self._state_store[domain][key]
                    if (now - state.timestamp).total_seconds() > ttl_seconds:
                        del self._state_store[domain][key]
                        logger.info(f"Flushed stale state: {domain}.{key}")

    def get_event_history(self, limit: int = 100) -> List[OrchestrationEvent]:
        """
        Returns recent orchestration events.
        """
        with self._lock:
            return self._history[-limit:]
