import asyncio
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from ecos.contracts.base import InstitutionalState, OrchestrationEvent, CognitiveOrigin
from ecos.core.event_bus import event_bus

logger = logging.getLogger("ecos.state.registry")

class InstitutionalStateRegistry:
    """
    Centralized registry for managing the global state of the ESOTERIC Cognitive OS.
    Ensures thread-safe access to institutional awareness.
    """
    
    def __init__(self):
        self._state_store: Dict[str, Dict[str, InstitutionalState]] = {}
        self._lock = asyncio.Lock()
        self._history: List[OrchestrationEvent] = []
        self._max_history = 1000

    async def set_state(self, domain: str, key: str, value: Any, metadata: Dict[str, Any] = None, origin: CognitiveOrigin = CognitiveOrigin.PRODUCTION) -> InstitutionalState:
        """
        Updates or creates a state entry within a specific domain.
        """
        async with self._lock:
            if domain not in self._state_store:
                self._state_store[domain] = {}
            
            state = InstitutionalState(
                domain=domain,
                key=key,
                value=value,
                origin=origin,
                metadata=metadata or {}
            )
            self._state_store[domain][key] = state
            
            # Log state change as an event
            event = OrchestrationEvent(
                source="StateRegistry",
                event_type="STATE_UPDATE",
                description=f"State updated: {domain}.{key}",
                severity="INFO",
                correlation_id=metadata.get("correlation_id") if metadata else None,
                metadata={
                    "domain": domain, 
                    "key": key, 
                    "value": str(value), # Convert to string for safe serialization
                    "origin": origin.name
                }
            )
            self._history.append(event)
            if len(self._history) > self._max_history:
                self._history.pop(0)
            
            logger.debug(f"State set: {domain}.{key}")
            
        # Publish event OUTSIDE the lock to avoid recursive deadlocks
        await event_bus.publish(event)
        
        return state

    async def get_state(self, domain: str, key: str) -> Optional[InstitutionalState]:
        """
        Retrieves a state entry.
        """
        async with self._lock:
            return self._state_store.get(domain, {}).get(key)

    async def get_domain_state(self, domain: str, origin: Optional[CognitiveOrigin] = None) -> Dict[str, Any]:
        """
        Retrieves all state entries for a specific domain, optionally filtered by origin.
        """
        async with self._lock:
            domain_data = self._state_store.get(domain, {})
            if origin:
                return {k: v.value for k, v in domain_data.items() if v.origin == origin}
            return {k: v.value for k, v in domain_data.items()}

    async def flush_stale_states(self, ttl_seconds: int):
        """
        Removes states that haven't been updated within the TTL.
        """
        now = datetime.utcnow()
        async with self._lock:
            for domain in list(self._state_store.keys()):
                for key in list(self._state_store[domain].keys()):
                    state = self._state_store[domain][key]
                    if (now - state.timestamp).total_seconds() > ttl_seconds:
                        del self._state_store[domain][key]
                        logger.info(f"Flushed stale state: {domain}.{key}")

    async def get_event_history(self, limit: int = 100) -> List[OrchestrationEvent]:
        """
        Returns recent orchestration events.
        """
        async with self._lock:
            return self._history[-limit:]
