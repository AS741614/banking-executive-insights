import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

from ai.actions.models.action_models import InstitutionalAction, ActionStatus, ApprovalTier, GovernanceWorkflow

logger = logging.getLogger("esoteric_bank.actions.workflow_engine")

class GovernanceWorkflowEngine:
    """
    Institutional Governance Workflow Engine.
    Manages the state transitions and approval gates for institutional actions.
    """

    def __init__(self):
        self._active_workflows: Dict[str, GovernanceWorkflow] = {}

    def start_workflow(self, workflow: GovernanceWorkflow):
        self._active_workflows[workflow.workflow_id] = workflow
        logger.info(f"Governance workflow initiated: {workflow.name} ({workflow.workflow_id})")

    async def approve_action(self, workflow_id: str, action_id: str, principal: str):
        """
        Processes a formal approval from an institutional principal.
        """
        workflow = self._active_workflows.get(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found.")

        for action in workflow.actions:
            if action.action_id == action_id:
                logger.info(f"Principal {principal} approved action {action_id} in workflow {workflow_id}")
                action.status = ActionStatus.APPROVED
                action.approved_by = principal
                action.approved_at = datetime.utcnow()
                
                workflow.audit_log.append({
                    "timestamp": action.approved_at.isoformat(),
                    "principal": principal,
                    "action": "APPROVED",
                    "action_id": action_id
                })
                break
        
        self._update_workflow_status(workflow)

    def _update_workflow_status(self, workflow: GovernanceWorkflow):
        # If all actions are approved/completed, workflow is considered progressing
        if all(a.status == ActionStatus.APPROVED for a in workflow.actions):
            workflow.overall_status = ActionStatus.APPROVED
            logger.info(f"Workflow {workflow.workflow_id} fully approved and ready for execution.")

    def get_pending_actions(self, tier: ApprovalTier) -> List[InstitutionalAction]:
        """Returns all actions requiring approval for a specific institutional tier."""
        pending = []
        for wf in self._active_workflows.values():
            for action in wf.actions:
                if action.status == ActionStatus.PROPOSED and action.required_approval_tier == tier:
                    pending.append(action)
        return pending
