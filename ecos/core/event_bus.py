import asyncio
import logging
from typing import Dict, List, Callable, Any, Awaitable
from ecos.contracts.base import OrchestrationEvent

logger = logging.getLogger("ecos.core.event_bus")

class EventBus:
    """
    Reactive event bus for live orchestration event propagation.
    Eliminates polling by providing a pub/sub mechanism for cognitive events.
    """
    
    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[OrchestrationEvent], Awaitable[None]]]] = {}
        self._lock = asyncio.Lock()

    async def subscribe(self, event_type: str, callback: Callable[[OrchestrationEvent], Awaitable[None]]):
        """
        Subscribes a callback to a specific event type.
        """
        async with self._lock:
            if event_type not in self._subscribers:
                self._subscribers[event_type] = []
            self._subscribers[event_type].append(callback)
            logger.debug(f"Subscribed to event: {event_type}")

    async def publish(self, event: OrchestrationEvent):
        """
        Publishes an event to all interested subscribers.
        """
        event_type = event.event_type
        subscribers = []
        
        async with self._lock:
            if event_type in self._subscribers:
                subscribers.extend(self._subscribers[event_type])
            # Also publish to wildcard subscribers
            if "*" in self._subscribers:
                subscribers.extend(self._subscribers["*"])

        if not subscribers:
            return

        # Execute all callbacks in parallel
        tasks = [callback(event) for callback in subscribers]
        await asyncio.gather(*tasks, return_exceptions=True)
        
        # Log any exceptions if needed (already handled by gather return_exceptions)
        logger.debug(f"Published event {event_type} to {len(subscribers)} subscribers.")

# Global instance for the ECOS core
event_bus = EventBus()
