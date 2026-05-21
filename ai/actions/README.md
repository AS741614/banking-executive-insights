# ESOTERIC BANK Action Orchestration & Governance Workflow

Institutional-grade infrastructure for governance-safe workflow orchestration and executive action coordination.

## Architecture
- **Framework**: Modular Python-based Workflow Orchestration
- **Core Principle**: Recommend-Not-Mutate (RNM) with mandatory Human-in-the-loop (HITL) approval gates.
- **Engine Layer**: Remediation Recommendation Engine and Governance Workflow Engine.
- **Auditability**: Full audit logs for every approval and action state transition.

## Core Subsystems

### 1. Remediation Recommendation Engine (`ai/actions/engines/remediation_engine.py`)
Reasons through risk signals from the `CognitiveEventBus` to propose specific institutional remediations (e.g., account suspension, policy realignment).

### 2. Governance Workflow Engine (`ai/actions/engines/workflow_engine.py`)
Manages the full lifecycle of institutional actions, enforcing approval tiers (Standard, Senior, Executive, Board) and maintaining an immutable audit trail.

### 3. Action Orchestration Service (`ai/actions/services/orchestration_service.py`)
The centralized coordinator that translates cognitive events into formal governance workflows.

## Action Workflow
1. **Detect**: A critical cognitive event is received (e.g., `FRAUD_DETECTED`).
2. **Propose**: The `RemediationRecommendationEngine` generates an `InstitutionalAction` with a clear "why."
3. **Initiate**: The `ActionOrchestrationService` starts a new `GovernanceWorkflow`.
4. **Approve**: An institutional principal (based on the required `ApprovalTier`) must explicitly approve the action.
5. **Execute**: Once approved, the action transitions to `EXECUTING` (ready for integration with automated execution layers).
6. **Audit**: Every state change is recorded in the workflow's audit log for regulatory compliance.

## Integration
This domain is fully compatible with the platform's distributed cognition layer and is designed to provide "Actionable Intelligence" to the Executive Command Center.
