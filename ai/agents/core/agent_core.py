import logging
import asyncio
import uuid
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime

from ai.agents.models.agent_models import (
    AgentType, 
    AgentStatus, 
    CognitiveMessage, 
    CognitiveTask
)
from ai.events.engines.event_bus import event_bus
from ai.events.models.event import CognitiveEvent, EventCategory, EventSeverity

logger = logging.getLogger("esoteric_bank.agents.core")

class CognitiveAgent(ABC):
    """
    Base class for all Institutional Cognitive Agents.
    Provides standard coordination and governance-aware reasoning interfaces.
    """
    
    def __init__(
        self, 
        agent_id: str, 
        agent_type: AgentType, 
        clearance: str = "TIER_1"
    ):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.clearance = clearance
        self.status = AgentStatus.IDLE
        self.message_history: List[CognitiveMessage] = []

    @abstractmethod
    async def process_message(self, message: CognitiveMessage):
        """Standard interface for handling inter-agent messages."""
        pass

    async def send_message(self, receiver_id: Optional[str], intent: str, content: Dict[str, Any], correlation_id: str):
        """Sends a message to another agent or broadcasts it."""
        message = CognitiveMessage(
            message_id=f"MSG-{uuid.uuid4().hex[:8].upper()}",
            sender_id=self.agent_id,
            receiver_id=receiver_id,
            correlation_id=correlation_id,
            intent=intent,
            content=content,
            governance_clearance=self.clearance
        )
        self.message_history.append(message)
        
        # Publish to the platform's event bus as a coordination event
        event = CognitiveEvent(
            event_id=message.message_id,
            trace_id=correlation_id,
            category=EventCategory.COGNITION,
            severity=EventSeverity.INFO,
            source_component=self.agent_id,
            action="AGENT_MESSAGE_SENT",
            payload={
                "intent": intent,
                "receiver": receiver_id or "BROADCAST",
                "content_summary": str(content)[:100]
            }
        )
        await event_bus.publish(event)
        return message

    def update_status(self, status: AgentStatus):
        self.status = status
        logger.debug(f"Agent {self.agent_id} status updated to {status}")

class AgentRegistry:
    """
    Institutional Agent Topology Registry.
    Tracks all active cognitive agents and their capabilities.
    """
    
    def __init__(self):
        self._agents: Dict[str, CognitiveAgent] = {}

    def register_agent(self, agent: CognitiveAgent):
        self._agents[agent.agent_id] = agent
        logger.info(f"Registered {agent.agent_type} agent: {agent.agent_id}")

    def get_agent(self, agent_id: str) -> Optional[CognitiveAgent]:
        return self._agents.get(agent_id)

    def list_agents_by_type(self, agent_type: AgentType) -> List[CognitiveAgent]:
        return [a for a in self._agents.values() if a.agent_type == agent_type]

    def list_all_agents(self) -> List[CognitiveAgent]:
        return list(self._agents.values())

# Global registry instance
agent_topology = AgentRegistry()
