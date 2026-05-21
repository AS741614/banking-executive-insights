import logging
import uuid
from typing import List, Dict, Any

from ai.agents.core.agent_core import CognitiveAgent, agent_topology
from ai.agents.models.agent_models import AgentType, AgentStatus, CognitiveMessage, CognitiveTask

logger = logging.getLogger("esoteric_bank.agents.orchestrator")

class InstitutionalOrchestratorAgent(CognitiveAgent):
    """
    Enterprise Cognitive Orchestrator.
    Manages collective intelligence workflows and agent collaboration.
    """
    
    def __init__(self, agent_id: str, clearance: str = "TIER_4"):
        super().__init__(agent_id, AgentType.ORCHESTRATOR, clearance)
        self.active_tasks: Dict[str, CognitiveTask] = {}

    async def process_message(self, message: CognitiveMessage):
        logger.info(f"Orchestrator {self.agent_id} received intent: {message.intent}")
        
        if message.intent == "TASK_REQUEST":
            await self._handle_task_request(message)
        elif message.intent == "TASK_UPDATE":
            await self._handle_task_update(message)

    async def _handle_task_request(self, message: CognitiveMessage):
        task_data = message.content.get("task")
        if not task_data:
            return

        task = CognitiveTask(
            task_id=f"TSK-{uuid.uuid4().hex[:8].upper()}",
            requester_id=message.sender_id,
            description=task_data.get("description", "No description"),
            context=task_data.get("context", {}),
            priority=task_data.get("priority", 1)
        )
        
        self.active_tasks[task.task_id] = task
        logger.info(f"Task {task.task_id} initialized. Routing to appropriate cognitive cluster.")
        
        # Simple routing logic based on description/type
        target_type = self._resolve_target_agent_type(task)
        agents = agent_topology.list_agents_by_type(target_type)
        
        if agents:
            target_agent = agents[0] # Pick the first available for now
            task.assigned_agent_id = target_agent.agent_id
            task.status = "ASSIGNED"
            
            await self.send_message(
                receiver_id=target_agent.agent_id,
                intent="TASK_ASSIGNMENT",
                content={"task_id": task.task_id, "details": task.model_dump()},
                correlation_id=message.correlation_id
            )
        else:
            logger.warning(f"No agents found for type: {target_type}")

    def _resolve_target_agent_type(self, task: CognitiveTask) -> AgentType:
        desc = task.description.upper()
        if "COMPLIANCE" in desc or "KYC" in desc or "AML" in desc:
            return AgentType.REGULATORY
        if "FRAUD" in desc or "ANOMALY" in desc:
            return AgentType.FRAUD
        return AgentType.GOVERNANCE

    async def _handle_task_update(self, message: CognitiveMessage):
        task_id = message.content.get("task_id")
        if task_id in self.active_tasks:
            self.active_tasks[task_id].status = message.content.get("status", "UPDATED")
            logger.info(f"Task {task_id} updated by {message.sender_id}")

class ComplianceAgent(CognitiveAgent):
    """
    Specialized Regulatory Compliance Agent.
    Focuses on governance-aware reasoning for KYC/AML tasks.
    """
    
    def __init__(self, agent_id: str):
        super().__init__(agent_id, AgentType.REGULATORY, "TIER_3")

    async def process_message(self, message: CognitiveMessage):
        if message.intent == "TASK_ASSIGNMENT":
            task_id = message.content.get("task_id")
            logger.info(f"Compliance Agent {self.agent_id} starting task: {task_id}")
            
            self.update_status(AgentStatus.BUSY)
            
            # Simulate institutional reasoning
            await asyncio.sleep(1) 
            
            await self.send_message(
                receiver_id=message.sender_id, # Usually back to orchestrator
                intent="TASK_UPDATE",
                content={"task_id": task_id, "status": "COMPLETED", "result": "Regulatory clearance granted."},
                correlation_id=message.correlation_id
            )
            
            self.update_status(AgentStatus.IDLE)

import asyncio
