import logging
import uuid
from typing import Dict, Any, List

from ai.actions.models.action_models import InstitutionalAction, GovernanceWorkflow, ActionStatus
from ai.actions.engines.remediation_engine import RemediationRecommendationEngine
from ai.actions.engines.workflow_engine import GovernanceWorkflowEngine
from ai.events.models.event import CognitiveEvent

logger = logging.getLogger("esoteric_bank.actions.orchestration_service")

class ActionOrchestrationService:
    """
    Enterprise Action Orchestration Service.
    Coordinates remediation recommendations and governance workflows.
    """

    def __init__(self):
        self.remediation_engine = RemediationRecommendationEngine()
        self.workflow_engine = GovernanceWorkflowEngine()

    async def orchestrate_event_response(self, event: CognitiveEvent) -> str:
        """
        Processes a cognitive event and orchestrates an institutional governance response.
        """
        logger.info(f"Orchestrating response for event: {event.action} (Trace: {event.trace_id})")

        # 1. Propose remediation
        action = self.remediation_engine.propose_remediation(event.payload, event.trace_id)

        # 2. Wrap in a formal Governance Workflow
        workflow = GovernanceWorkflow(
            workflow_id=f"WF-{uuid.uuid4().hex[:8].upper()}",
            name=f"Governance Response: {event.action}",
            description=f"Institutional response triggered by {event.source_component}.",
            actions=[action]
        )

        # 3. Start Workflow
        self.workflow_engine.start_workflow(workflow)
        
        logger.info(f"Orchestration complete. Workflow {workflow.workflow_id} is PENDING_APPROVAL.")
        return workflow.workflow_id

    def get_action_registry_state(self) -> Dict[str, Any]:
        """Returns the current state of all active actions and workflows."""
        return {
            "active_workflows_count": len(self.workflow_engine._active_workflows),
            "pending_approvals": len(self.workflow_engine.get_pending_actions("TIER_1_STANDARD")) + \
                                 len(self.workflow_engine.get_pending_actions("TIER_3_EXECUTIVE"))
        }
