import logging
from typing import List, Dict, Any
from ecos.contracts.base import CognitiveTask, CognitiveTaskPriority, OrchestrationEvent
from ecos.state.registry import InstitutionalStateRegistry

logger = logging.getLogger("ecos.governance.continuity")

class GovernanceContinuityLayer:
    """
    Ensures governance continuity and policy enforcement within the ESOTERIC Cognitive OS.
    Acts as a supervisor for the Runtime Coordinator.
    """
    
    def __init__(self, state_registry: InstitutionalStateRegistry):
        self.state = state_registry
        self._policy_registry: Dict[str, Any] = {
            "max_task_latency": 60,
            "restricted_domains": ["core_ledger", "untested_ai_models"],
            "critical_priority_required_for": ["system_reboot", "global_freeze"]
        }

    async def handle_state_update(self, event: OrchestrationEvent):
        """
        Proactively handles state update events to adjust governance posture.
        """
        domain = event.metadata.get("domain")
        key = event.metadata.get("key")
        value = event.metadata.get("value")
        
        if domain == "system" and key == "runtime_status":
            if value == "DEGRADED":
                logger.warning("Governance Posture: AUTOMATIC ESCALATION triggered due to DEGRADED system status.")
                # Automatically tighten policies
                await self.update_policy("max_task_latency", 10)
            elif value == "OPERATIONAL":
                logger.info("Governance Posture: NORMALIZING due to OPERATIONAL system status.")
                await self.update_policy("max_task_latency", 60)

    async def validate_task(self, task: CognitiveTask) -> bool:
        """
        Validates a task against institutional governance policies.
        """
        logger.debug(f"Governing task validation for: {task.task_id}")
        
        # Rule 1: Restricted Domains
        if task.service_domain in self._policy_registry["restricted_domains"]:
            self._log_violation(task, "RESTRICTED_DOMAIN_ACCESS")
            return False
            
        # Rule 2: Priority Check for critical actions
        if task.action in self._policy_registry["critical_priority_required_for"] and \
           task.priority != CognitiveTaskPriority.CRITICAL:
            self._log_violation(task, "INSUFFICIENT_PRIORITY")
            return False
            
        # Rule 3: Execution Context Check
        system_status = await self.state.get_state("system", "runtime_status")
        if system_status and system_status.value == "DEGRADED" and task.priority == CognitiveTaskPriority.LOW:
            logger.warning(f"Task {task.task_id} suppressed due to DEGRADED system state.")
            return False

        return True

    def _log_violation(self, task: CognitiveTask, violation_type: str):
        """
        Logs a governance policy violation.
        """
        logger.error(f"Governance Violation: {violation_type} | Task: {task.task_id}")
        event = OrchestrationEvent(
            source="GovernanceContinuity",
            event_type="POLICY_VIOLATION",
            description=f"Task rejected due to {violation_type}",
            severity="CRITICAL",
            metadata={"task_id": task.task_id, "domain": task.service_domain, "action": task.action}
        )
        # Store in state registry history
        # (Assuming the registry instance is shared)
        # In a real system, this would be an atomic update.

    async def update_policy(self, policy_key: str, value: Any):
        """
        Updates a governance policy dynamically.
        """
        logger.info(f"Governance Policy Updated: {policy_key} = {value}")
        self._policy_registry[policy_key] = value
        await self.state.set_state(
            domain="governance",
            key=f"policy_{policy_key}",
            value=value,
            metadata={"updated_at": datetime.utcnow().isoformat()}
        )

from datetime import datetime
