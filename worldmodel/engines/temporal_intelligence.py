import logging
from collections import defaultdict
from typing import List, Dict, Any
from worldmodel.models.world_models import TemporalState

logger = logging.getLogger("esoteric_bank.worldmodel.temporal_intelligence")

class TemporalStateIntelligence:
    """
    Enterprise Temporal State Intelligence.
    Tracks and retrieves the historical evolution of institutional state.
    """

    def __init__(self):
        # Local in-memory timeline (indexed by entity_id)
        self._timeline: Dict[str, List[TemporalState]] = defaultdict(list)

    def record_state_transition(self, state: TemporalState):
        self._timeline[state.entity_id].append(state)
        # Keep timeline sorted by timestamp
        self._timeline[state.entity_id].sort(key=lambda x: x.timestamp)
        logger.debug(f"Recorded state transition for {state.entity_id}: {state.attribute_name}={state.value}")

    def get_latest_state(self, entity_id: str, attribute_name: str) -> Optional[TemporalState]:
        history = self._timeline.get(entity_id, [])
        for state in reversed(history):
            if state.attribute_name == attribute_name:
                return state
        return None

    def get_historical_snapshot(self, entity_id: str, timestamp: datetime) -> Dict[str, Any]:
        """Reconstructs the state of an entity at a specific point in time."""
        snapshot = {}
        history = self._timeline.get(entity_id, [])
        for state in history:
            if state.timestamp <= timestamp:
                snapshot[state.attribute_name] = state.value
            else:
                break
        return snapshot

from datetime import datetime
from typing import Optional
