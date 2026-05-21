import asyncio
import logging
from typing import List, Dict, Any
from ai.events.engines.event_bus import event_bus
from ai.events.models.event import CognitiveEvent

logger = logging.getLogger("esoteric_bank.demo.replay")

class InstitutionalReplayEngine:
    """
    Engine for replaying institutional event sequences.
    Enables post-mortem executive review and demo consistency.
    """

    async def replay_sequence(self, event_logs: List[Dict[str, Any]], speed_factor: float = 1.0):
        """
        Replays a sequence of logged events.
        """
        logger.info(f"--- STARTING INSTITUTIONAL REPLAY (Speed: {speed_factor}x) ---")
        
        for event_dict in event_logs:
            # Reconstruct event
            event = CognitiveEvent(**event_dict)
            
            logger.info(f"Replaying: {event.action} ({event.event_id})")
            await event_bus.publish(event)
            
            # Simulate original timing (mocked for now, could use timestamps)
            delay = 2.0 / speed_factor
            await asyncio.sleep(delay)

        logger.info("--- INSTITUTIONAL REPLAY COMPLETE ---")
