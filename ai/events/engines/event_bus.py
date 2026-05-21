import logging
import asyncio
from typing import List, Callable, Dict, Any
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

    def subscribe(self, category: Any, callback: Callable):
        cat_key = str(category.value) if hasattr(category, "value") else str(category)
        if cat_key not in self._subscribers:
            self._subscribers[cat_key] = []
        self._subscribers[cat_key].append(callback)
        logger.debug(f"[BUS_{id(self)}] Subscriber registered for category: {cat_key}")

    async def publish(self, event: CognitiveEvent):
        """
        Publishes an event to all interested subscribers.
        """
        self._event_history.append(event)
        cat_key = str(event.category.value) if hasattr(event.category, "value") else str(event.category)
        logger.info(f"[BUS_{id(self)}] Event Published: {event.event_id} | Category: {cat_key} | Action: {event.action}")
        
        # In a real system, this would be an async dispatch to a queue (e.g., Kafka)
        if cat_key in self._subscribers:
            tasks = [callback(event) for callback in self._subscribers[cat_key]]
            await asyncio.gather(*tasks, return_exceptions=True)

    def get_history(self, limit: int = 100) -> List[CognitiveEvent]:
        return self._event_history[-limit:]

# Global Singleton for the platform
event_bus = CognitiveEventBus()
