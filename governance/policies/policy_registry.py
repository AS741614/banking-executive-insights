"""The institutional policy registry.

These rules were previously hardcoded inside `ai/fraud/engines/fraud_engine.py`.
They are declared here instead, for three reasons that matter to a reviewer:

  1. Policy expressed as data can be read and challenged by someone who does
     not read Python. Policy buried in a scoring function cannot.
  2. Every policy carries an id and a revision, so a finding can be traced to
     the exact rule version that produced it.
  3. The rules can be listed, diffed and reviewed without executing anything.

Source of truth: governance/controls/institutional_overrides.md (GOV-CTRL-FRAUD-001)
and governance/constitution/institutional_sovereignty_constitution.md.

Adding a policy means adding an entry here - not editing the fraud engine.
"""
from __future__ import annotations

from typing import Any, Callable, Dict, List

from pydantic import BaseModel, ConfigDict, Field

from governance.contracts import GovernanceAction, Severity

# A predicate reads a flat dict of signals and answers: did this rule match?
Predicate = Callable[[Dict[str, Any]], bool]


class Policy(BaseModel):
    """One institutional rule.

    `condition` is excluded from serialisation - the *description* is what goes
    into an audit record, because a lambda is not evidence.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    policy_id: str
    title: str
    revision: str
    article_ref: str
    severity: Severity
    action: GovernanceAction
    condition_description: str
    condition: Predicate = Field(exclude=True)
    # A non-nettable policy forces the overall outcome regardless of how
    # favourable everything else looks. Some findings are disqualifying.
    non_nettable: bool = False

    def matches(self, signals: Dict[str, Any]) -> bool:
        try:
            return bool(self.condition(signals))
        except (KeyError, TypeError):
            # A missing signal is not a match, but it is also not silence:
            # the engine records unevaluable policies separately.
            raise


def _get(signals: Dict[str, Any], key: str, default: Any = None) -> Any:
    return signals.get(key, default)


# ---------------------------------------------------------------------------
# GOV-CTRL-FRAUD-001 - Critical hardware threat overrides
# ---------------------------------------------------------------------------

FRAUD_POLICIES: List[Policy] = [
    Policy(
        policy_id="GOV-CTRL-FRAUD-001.1",
        title="Emulator detected on originating device",
        revision="1.1",
        article_ref="Constitution Art. I - Governance Primacy",
        severity=Severity.CRITICAL,
        action=GovernanceAction.BLOCK,
        condition_description="device.emulator_detected is true",
        condition=lambda s: bool(_get(s, "emulator_detected", False)),
        non_nettable=True,
    ),
    Policy(
        policy_id="GOV-CTRL-FRAUD-001.2",
        title="Origination from a TOR exit node",
        revision="1.1",
        article_ref="Constitution Art. I - Governance Primacy",
        severity=Severity.CRITICAL,
        action=GovernanceAction.BLOCK,
        condition_description="device.tor_detected is true",
        condition=lambda s: bool(_get(s, "tor_detected", False)),
        non_nettable=True,
    ),
    Policy(
        policy_id="GOV-CTRL-FRAUD-001.3",
        title="High-risk VPN origination",
        revision="1.1",
        article_ref="Constitution Art. I - Governance Primacy",
        severity=Severity.HIGH,
        action=GovernanceAction.CHALLENGE,
        condition_description="device.vpn_risk_score > 0.9",
        condition=lambda s: float(_get(s, "vpn_risk_score", 0.0)) > 0.9,
    ),
    Policy(
        policy_id="GOV-CTRL-FRAUD-001.4",
        title="Impossible travel (geographic drift with velocity variance)",
        revision="1.1",
        article_ref="Constitution Art. I - Governance Primacy",
        severity=Severity.CRITICAL,
        action=GovernanceAction.BLOCK,
        condition_description="geographical_drift is true AND velocity_variance > 2.0",
        condition=lambda s: bool(_get(s, "geographical_drift", False))
        and float(_get(s, "velocity_variance", 0.0)) > 2.0,
        non_nettable=True,
    ),
]

# ---------------------------------------------------------------------------
# GOV-CTRL-FRAUD-001 - AML compliance overrides
# ---------------------------------------------------------------------------

AML_POLICIES: List[Policy] = [
    Policy(
        policy_id="GOV-CTRL-AML-001.1",
        title="Regulatory watchlist match",
        revision="1.1",
        article_ref="Constitution Art. IV - Regulatory Alignment",
        severity=Severity.CRITICAL,
        action=GovernanceAction.HOLD,
        condition_description="regulatory_watchlist_flag is true",
        condition=lambda s: bool(_get(s, "regulatory_watchlist_flag", False)),
        non_nettable=True,
    ),
    Policy(
        policy_id="GOV-CTRL-AML-001.2",
        title="Digital structuring pattern",
        revision="1.1",
        article_ref="Constitution Art. IV - Regulatory Alignment",
        severity=Severity.HIGH,
        action=GovernanceAction.ESCALATE,
        condition_description="structuring_score > 0.9",
        condition=lambda s: float(_get(s, "structuring_score", 0.0)) > 0.9,
        non_nettable=True,
    ),
    Policy(
        policy_id="GOV-CTRL-AML-001.3",
        title="Layering pattern across accounts",
        revision="1.1",
        article_ref="Constitution Art. IV - Regulatory Alignment",
        severity=Severity.HIGH,
        action=GovernanceAction.ESCALATE,
        condition_description="layering_score > 0.85",
        condition=lambda s: float(_get(s, "layering_score", 0.0)) > 0.85,
    ),
]

ALL_POLICIES: List[Policy] = FRAUD_POLICIES + AML_POLICIES


def registry() -> List[Policy]:
    """Every active policy. Ordered, so evaluation is deterministic."""
    return list(ALL_POLICIES)


def describe() -> List[Dict[str, str]]:
    """A reviewable, code-free listing of the rulebook.

    This is what you hand someone who wants to audit the policy set without
    reading the implementation.
    """
    return [
        {
            "policy_id": p.policy_id,
            "title": p.title,
            "revision": p.revision,
            "article": p.article_ref,
            "severity": p.severity.value,
            "action": p.action.value,
            "condition": p.condition_description,
            "non_nettable": "yes" if p.non_nettable else "no",
        }
        for p in ALL_POLICIES
    ]
