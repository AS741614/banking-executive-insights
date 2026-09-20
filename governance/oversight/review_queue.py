"""Constitution Article V - human oversight, made executable.

Article V reserves ultimate authority to a human. That only means something if
there is somewhere for a decision to wait, and a record of what the human
actually decided. Without the second half, "human in the loop" is decoration.

Three rules this queue enforces:

  1. A CRITICAL item cannot be auto-closed. It stays open until a named
     reviewer records a decision. That is the kill-switch.
  2. Every decision captures who made it, when, and why. A reviewer verdict
     with no rationale is not an audit trail.
  3. Overturning an automated decision is recorded as such, separately from
     upholding it - because the rate at which humans overturn the system is
     itself a governance metric worth watching.
"""
from __future__ import annotations

import json
import logging
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from governance.contracts import (
    ExplanationRecord,
    GovernanceAction,
    OversightItem,
    ReviewDecision,
    Severity,
)
from governance.policies.policy_engine import PolicyEvaluation

logger = logging.getLogger("esoteric_bank.governance.oversight")

# At or above this severity, a human must sign off before the item closes.
MANDATORY_REVIEW_AT = Severity.HIGH


class ReviewQueueError(RuntimeError):
    """Raised when an action would breach an oversight rule."""


class ReviewQueue:
    """An auditable queue of decisions awaiting human judgement."""

    def __init__(self, store_path: Optional[str | Path] = None):
        self._items: Dict[str, OversightItem] = {}
        self._store = Path(store_path) if store_path else None
        if self._store and self._store.exists():
            self._load()

    # -- submission ---------------------------------------------------------

    def requires_review(self, severity: Severity | str) -> bool:
        return Severity.rank(severity) >= Severity.rank(MANDATORY_REVIEW_AT)

    def submit(
        self,
        subject_id: str,
        evaluation: PolicyEvaluation,
        explanation: Optional[ExplanationRecord] = None,
    ) -> Optional[OversightItem]:
        """Queue an item if its severity warrants human review.

        Returns None when no review is required - the caller can proceed.
        """
        severity = Severity(evaluation.overall_severity)
        if not self.requires_review(severity):
            return None

        item = OversightItem(
            item_id=f"OVS-{uuid.uuid4().hex[:8].upper()}",
            subject_id=subject_id,
            severity=severity,
            proposed_action=GovernanceAction(evaluation.overall_action),
            reason=evaluation.non_nettable_override
            or f"{len(evaluation.triggered)} policy finding(s) at {severity.value}.",
            explanation_id=explanation.explanation_id if explanation else None,
            policies_applied=[o.policy_id for o in evaluation.triggered],
        )

        self._items[item.item_id] = item
        self._persist()
        logger.info(
            "Oversight item %s raised for %s at %s",
            item.item_id,
            subject_id,
            severity.value,
        )
        return item

    # -- review -------------------------------------------------------------

    def record_decision(
        self,
        item_id: str,
        decision: ReviewDecision,
        reviewer: str,
        rationale: str,
    ) -> OversightItem:
        item = self._items.get(item_id)
        if item is None:
            raise ReviewQueueError(f"No oversight item with id {item_id}.")

        if not item.is_open:
            raise ReviewQueueError(
                f"{item_id} was already decided ({item.decision}). "
                "Reopen it explicitly rather than overwriting the record."
            )

        if decision == ReviewDecision.PENDING:
            raise ReviewQueueError("PENDING is not a decision.")

        if not reviewer or not rationale.strip():
            # Rule 2: a verdict without a named reviewer and a reason is not
            # an audit trail, so refuse to record it.
            raise ReviewQueueError(
                "A review decision requires both a named reviewer and a rationale."
            )

        item.decision = decision
        item.reviewer = reviewer
        item.reviewer_rationale = rationale.strip()
        item.decided_at = datetime.now(timezone.utc)

        self._persist()
        logger.info(
            "Oversight item %s %s by %s", item_id, decision.value, reviewer
        )
        return item

    # -- inspection ---------------------------------------------------------

    def pending(self) -> List[OversightItem]:
        return sorted(
            (i for i in self._items.values() if i.is_open),
            key=lambda i: Severity.rank(i.severity),
            reverse=True,
        )

    def get(self, item_id: str) -> Optional[OversightItem]:
        return self._items.get(item_id)

    def all_items(self) -> List[OversightItem]:
        return list(self._items.values())

    def override_rate(self) -> float:
        """Share of decided items where the human reversed the system.

        A governance metric in its own right: a rate near zero may mean the
        system is well calibrated, or that review has become a rubber stamp.
        Either way it is worth watching.
        """
        decided = [i for i in self._items.values() if not i.is_open]
        if not decided:
            return 0.0
        overturned = sum(
            1 for i in decided if i.decision == ReviewDecision.OVERTURNED.value
        )
        return round(overturned / len(decided), 4)

    def summary(self) -> Dict[str, object]:
        return {
            "total": len(self._items),
            "open": len(self.pending()),
            "critical_open": sum(
                1
                for i in self.pending()
                if Severity(i.severity) == Severity.CRITICAL
            ),
            "override_rate": self.override_rate(),
        }

    # -- persistence --------------------------------------------------------

    def _persist(self) -> None:
        if not self._store:
            return
        self._store.parent.mkdir(parents=True, exist_ok=True)
        payload = [i.model_dump(mode="json") for i in self._items.values()]
        self._store.write_text(json.dumps(payload, indent=2, default=str))

    def _load(self) -> None:
        try:
            data = json.loads(self._store.read_text())
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning("Could not load oversight store: %s", exc)
            return
        for row in data:
            item = OversightItem(**row)
            self._items[item.item_id] = item
