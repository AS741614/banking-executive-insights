"""Policy evaluation.

Two rules govern how outcomes combine, and both are deliberate:

  1. EVERY matching policy is recorded, not just the worst one. The severity
     that wins is the highest, but the others remain in the audit trail -
     you cannot review a decision if the evidence was discarded on the way.

  2. A non-nettable policy forces the overall outcome. A CRITICAL finding is
     not averaged against favourable signals elsewhere; some findings are
     disqualifying regardless of the rest of the picture.

An unevaluable policy - one whose required signal is absent - is reported as
unevaluable rather than silently treated as "did not match". Missing evidence
and negative evidence are different things.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel, ConfigDict, Field

from governance.contracts import GovernanceAction, PolicyOutcome, Severity
from governance.policies.policy_registry import Policy, registry

logger = logging.getLogger("esoteric_bank.governance.policy_engine")


class PolicyEvaluation(BaseModel):
    """The full result of running the rulebook against one set of signals."""

    model_config = ConfigDict(use_enum_values=True)

    overall_severity: Severity
    overall_action: GovernanceAction
    triggered: List[PolicyOutcome] = Field(default_factory=list)
    non_nettable_override: Optional[str] = None
    unevaluable: List[str] = Field(default_factory=list)

    @property
    def clean(self) -> bool:
        return not self.triggered and not self.unevaluable


# Which action is more restrictive, when several policies fire at once.
_ACTION_PRECEDENCE = [
    GovernanceAction.MONITOR,
    GovernanceAction.CHALLENGE,
    GovernanceAction.ESCALATE,
    GovernanceAction.HOLD,
    GovernanceAction.BLOCK,
]


def _strictest(actions: List[GovernanceAction]) -> GovernanceAction:
    if not actions:
        return GovernanceAction.MONITOR
    return max(actions, key=lambda a: _ACTION_PRECEDENCE.index(GovernanceAction(a)))


class PolicyEngine:
    """Evaluates the institutional rulebook against a flat signal dictionary."""

    def __init__(self, policies: Optional[List[Policy]] = None):
        self.policies = policies if policies is not None else registry()

    def evaluate(self, signals: Dict[str, Any]) -> PolicyEvaluation:
        triggered: List[PolicyOutcome] = []
        unevaluable: List[str] = []

        for policy in self.policies:
            try:
                matched = policy.matches(signals)
            except (KeyError, TypeError) as exc:
                # Record it - do not let a missing signal look like a pass.
                logger.warning(
                    "Policy %s could not be evaluated: %s", policy.policy_id, exc
                )
                unevaluable.append(policy.policy_id)
                continue

            if not matched:
                continue

            triggered.append(
                PolicyOutcome(
                    policy_id=policy.policy_id,
                    policy_title=policy.title,
                    policy_revision=policy.revision,
                    triggered=True,
                    severity=policy.severity,
                    action=policy.action,
                    triggering_signals=self._relevant_signals(policy, signals),
                    rationale=policy.condition_description,
                    non_nettable=policy.non_nettable,
                )
            )

        severity, action, override = self._combine(triggered)

        return PolicyEvaluation(
            overall_severity=severity,
            overall_action=action,
            triggered=triggered,
            non_nettable_override=override,
            unevaluable=unevaluable,
        )

    def _combine(
        self, triggered: List[PolicyOutcome]
    ) -> Tuple[Severity, GovernanceAction, Optional[str]]:
        if not triggered:
            return Severity.INFORMATIONAL, GovernanceAction.MONITOR, None

        # Non-nettable findings decide the outcome on their own.
        blocking = [o for o in triggered if o.non_nettable]
        if blocking:
            worst = max(blocking, key=lambda o: Severity.rank(o.severity))
            return (
                Severity(worst.severity),
                GovernanceAction(worst.action),
                f"{worst.policy_id} is non-nettable and forced the outcome.",
            )

        severity = Severity.highest([o.severity for o in triggered])
        action = _strictest([GovernanceAction(o.action) for o in triggered])
        return severity, action, None

    @staticmethod
    def _relevant_signals(policy: Policy, signals: Dict[str, Any]) -> Dict[str, Any]:
        """Capture only the signals the policy's condition actually names.

        Keeps the audit record proportionate - the whole payload is noise.
        """
        return {
            key: value
            for key, value in signals.items()
            if key in policy.condition_description
        }
