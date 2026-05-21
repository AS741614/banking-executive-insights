import asyncio
import logging
import uuid
from typing import List, Dict, Any, Callable
from ai.events.models.event import CognitiveEvent

logger = logging.getLogger("esoteric_bank.events.streaming_bus")

class CognitiveEventStreamer:
    """
    Enterprise Cognitive Event Bus with Live Streaming Capabilities.
    Supports both standard pub/sub and asynchronous event streaming.
    """
    
    def __init__(self):
        self._subscribers: List[asyncio.Queue] = []
        self._history: List[CognitiveEvent] = []
        self._max_history = 500

    async def publish(self, event: CognitiveEvent):
        """Publishes an event to the internal history and all active stream queues."""
        self._history.append(event)
        if len(self._history) > self._max_history:
            self._history.pop(0)

        logger.info(f"Streaming Event: {event.event_id} | {event.action}")
        
        # Dispatch to all active stream queues
        for queue in self._subscribers:
            await queue.put(event)

    def subscribe(self) -> asyncio.Queue:
        """Creates a new subscription queue for live streaming."""
        queue = asyncio.Queue()
        self._subscribers.append(queue)
        return queue

    def unsubscribe(self, queue: asyncio.Queue):
        """Removes an active subscription."""
        if queue in self._subscribers:
            self._subscribers.remove(queue)

    def get_recent_history(self, limit: int = 50) -> List[CognitiveEvent]:
        return self._history[-limit:]

# Global Singleton for Platform Streaming
event_streamer = CognitiveEventStreamer()
