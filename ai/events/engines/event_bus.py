import logging
import asyncio
from typing import List, Callable, Dict
from ai.events.models.event import CognitiveEvent

logger = logging.getLogger("esoteric_bank.events.event_bus")

class CognitiveEventBus:
    """
    Enterprise Cognitive Event Bus.
    Handles distribution of governance and operational events.
    """
    
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
        self._event_history: List[CognitiveEvent] = []

    def subscribe(self, category: str, callback: Callable):
        if category not in self._subscribers:
            self._subscribers[category] = []
        self._subscribers[category].append(callback)
        logger.debug(f"Subscriber registered for category: {category}")

    async def publish(self, event: CognitiveEvent):
        """
        Publishes an event to all interested subscribers.
        """
        self._event_history.append(event)
        logger.info(f"Event Published: {event.event_id} | Category: {event.category} | Action: {event.action}")
        
        # In a real system, this would be an async dispatch to a queue (e.g., Kafka)
        if event.category in self._subscribers:
            tasks = [callback(event) for callback in self._subscribers[event.category]]
            await asyncio.gather(*tasks, return_exceptions=True)

    def get_history(self, limit: int = 100) -> List[CognitiveEvent]:
        return self._event_history[-limit:]

# Global Singleton for the platform
event_bus = CognitiveEventBus()
