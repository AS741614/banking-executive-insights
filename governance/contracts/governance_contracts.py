"""Shared governance contracts.

Every other governance module depends on these types and nothing else, so the
policy engine, the explanation builder and the oversight queue can evolve
independently without drifting apart on what a "finding" actually is.

Design note: severity is an ordered enum rather than a float. A governance
finding is a classification, not a measurement - averaging two findings is
never meaningful, and an ordered enum makes that impossible by construction.
"""
from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, confloat


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Severity(str, Enum):
    """Ordered severity. Compare with `Severity.rank()`, never alphabetically."""

    INFORMATIONAL = "INFORMATIONAL"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

    @classmethod
    def rank(cls, value: "Severity | str") -> int:
        order = [
            cls.INFORMATIONAL,
            cls.LOW,
            cls.MEDIUM,
            cls.HIGH,
            cls.CRITICAL,
        ]
        return order.index(cls(value))

    @classmethod
    def highest(cls, values: List["Severity | str"]) -> "Severity":
        if not values:
            return cls.INFORMATIONAL
        return cls(max(values, key=cls.rank))


class GovernanceAction(str, Enum):
    """What the institution does in response to a finding."""

    MONITOR = "MONITOR"
    CHALLENGE = "CHALLENGE"
    HOLD = "HOLD"
    BLOCK = "BLOCK"
    ESCALATE = "ESCALATE"


class PolicyOutcome(BaseModel):
    """The result of evaluating one policy against one set of signals.

    Carries the policy identity and revision, not just the verdict - a finding
    you cannot trace back to the exact policy version that produced it is not
    auditable.
    """

    model_config = ConfigDict(use_enum_values=True)

    policy_id: str
    policy_title: str
    policy_revision: str
    triggered: bool
    severity: Severity
    action: GovernanceAction
    # The signal values that actually caused the match, for the audit trail.
    triggering_signals: Dict[str, Any] = Field(default_factory=dict)
    rationale: str = ""
    non_nettable: bool = False
    evaluated_at: datetime = Field(default_factory=_utcnow)


class FactorAttribution(BaseModel):
    """One contributing factor behind a decision, and how much it mattered."""

    factor: str
    value: Any
    contribution: confloat(ge=0.0, le=1.0)
    direction: str = "increases_risk"  # or "reduces_risk"
    note: Optional[str] = None


class ExplanationRecord(BaseModel):
    """Constitution Article III made executable.

    An explanation is not a log line. It has to answer three questions:
    what was decided, which factors drove it, and under which policy - all
    tied to a trace ID so the decision can be reconstructed later.
    """

    model_config = ConfigDict(use_enum_values=True)

    explanation_id: str
    subject_id: str  # e.g. the fraud assessment or model run being explained
    decision: GovernanceAction
    severity: Severity
    narrative: str
    factors: List[FactorAttribution] = Field(default_factory=list)
    policies_applied: List[str] = Field(default_factory=list)
    trace_id: Optional[str] = None
    created_at: datetime = Field(default_factory=_utcnow)

    def top_factors(self, n: int = 3) -> List[FactorAttribution]:
        return sorted(self.factors, key=lambda f: f.contribution, reverse=True)[:n]


class ReviewDecision(str, Enum):
    PENDING = "PENDING"
    UPHELD = "UPHELD"          # reviewer agrees with the automated decision
    OVERTURNED = "OVERTURNED"  # reviewer disagrees and reverses it
    ESCALATED = "ESCALATED"    # reviewer sends it further up


class OversightItem(BaseModel):
    """Something a human has to look at before it is considered closed.

    `validate_assignment` matters here: this model is mutated after creation
    when a reviewer records a decision, and without it the enum would be
    stored as an object rather than coerced to its value.
    """

    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)

    item_id: str
    subject_id: str
    severity: Severity
    proposed_action: GovernanceAction
    reason: str
    explanation_id: Optional[str] = None
    policies_applied: List[str] = Field(default_factory=list)

    decision: ReviewDecision = ReviewDecision.PENDING
    reviewer: Optional[str] = None
    reviewer_rationale: Optional[str] = None
    raised_at: datetime = Field(default_factory=_utcnow)
    decided_at: Optional[datetime] = None

    @property
    def is_open(self) -> bool:
        return self.decision == ReviewDecision.PENDING.value
