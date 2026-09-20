"""Constitution Article III, made executable.

Article III requires that every autonomous decision carries "the cognitive
reasoning, the governance policy applied, and the trace ID". That was a
statement of intent with no implementation behind it. This module produces it.

What an explanation has to do, to be worth anything:

  * name the factors that actually drove the decision, with their weights,
    rather than restating the outcome in longer words
  * cite the policies by id AND revision, so the decision can be reconstructed
    against the rulebook as it stood at the time
  * carry a trace id, so it joins up with the event stream and the audit log
  * be generated from the same inputs the decision used - an explanation
    produced from different data is a story, not an explanation
"""
from __future__ import annotations

import logging
import uuid
from typing import Any, Dict, List, Optional

from governance.contracts import (
    ExplanationRecord,
    FactorAttribution,
    GovernanceAction,
    Severity,
)
from governance.policies.policy_engine import PolicyEvaluation

logger = logging.getLogger("esoteric_bank.governance.explainability")


# How much each signal contributes when it is present. These are documented
# weights, not learned ones - stated plainly so a reviewer can challenge them.
FACTOR_WEIGHTS: Dict[str, float] = {
    "emulator_detected": 1.00,
    "tor_detected": 0.95,
    "regulatory_watchlist_flag": 0.95,
    "geographical_drift": 0.70,
    "structuring_score": 0.85,
    "layering_score": 0.80,
    "vpn_risk_score": 0.60,
    "velocity_variance": 0.55,
    "proxy_detected": 0.40,
    "unusual_time_pattern": 0.30,
    "amount_variance": 0.30,
}

FACTOR_LABELS: Dict[str, str] = {
    "emulator_detected": "transaction originated from an emulated device",
    "tor_detected": "transaction originated from a TOR exit node",
    "regulatory_watchlist_flag": "customer matched a regulatory watchlist",
    "geographical_drift": "location inconsistent with recent activity",
    "structuring_score": "transaction pattern consistent with structuring",
    "layering_score": "transaction pattern consistent with layering",
    "vpn_risk_score": "originating network flagged as high-risk VPN",
    "velocity_variance": "transaction velocity outside the customer baseline",
    "proxy_detected": "originating network is a proxy",
    "unusual_time_pattern": "activity outside the customer's usual hours",
    "amount_variance": "amount outside the customer's usual range",
}


class ExplanationBuilder:
    """Turns signals plus a policy evaluation into an auditable explanation."""

    def build(
        self,
        subject_id: str,
        signals: Dict[str, Any],
        evaluation: PolicyEvaluation,
        trace_id: Optional[str] = None,
    ) -> ExplanationRecord:
        factors = self._attribute(signals)
        narrative = self._narrate(evaluation, factors)

        record = ExplanationRecord(
            explanation_id=f"EXP-{uuid.uuid4().hex[:8].upper()}",
            subject_id=subject_id,
            decision=GovernanceAction(evaluation.overall_action),
            severity=Severity(evaluation.overall_severity),
            narrative=narrative,
            factors=factors,
            policies_applied=[
                f"{o.policy_id}@{o.policy_revision}" for o in evaluation.triggered
            ],
            trace_id=trace_id,
        )

        logger.info(
            "Explanation %s built for %s (%s, %d factors, %d policies)",
            record.explanation_id,
            subject_id,
            record.decision,
            len(factors),
            len(record.policies_applied),
        )
        return record

    def _attribute(self, signals: Dict[str, Any]) -> List[FactorAttribution]:
        """One attribution per signal that is present and actually active."""
        factors: List[FactorAttribution] = []

        for key, weight in FACTOR_WEIGHTS.items():
            if key not in signals:
                continue

            raw = signals[key]
            if isinstance(raw, bool):
                if not raw:
                    continue
                contribution = weight
            else:
                try:
                    numeric = float(raw)
                except (TypeError, ValueError):
                    continue
                if numeric <= 0:
                    continue
                # Scale the weight by the signal, capped at its documented max.
                contribution = min(weight, weight * min(numeric, 1.0) if numeric <= 1.0 else weight)

            factors.append(
                FactorAttribution(
                    factor=key,
                    value=raw,
                    contribution=round(contribution, 4),
                    direction="increases_risk",
                    note=FACTOR_LABELS.get(key),
                )
            )

        return sorted(factors, key=lambda f: f.contribution, reverse=True)

    def _narrate(
        self, evaluation: PolicyEvaluation, factors: List[FactorAttribution]
    ) -> str:
        if evaluation.clean:
            return (
                "No institutional policy was triggered and no risk factors were "
                "present. Decision: monitor only."
            )

        parts: List[str] = []

        if evaluation.non_nettable_override:
            parts.append(
                f"Outcome forced by a non-nettable finding. "
                f"{evaluation.non_nettable_override}"
            )
        else:
            parts.append(
                f"{len(evaluation.triggered)} "
                f"{'policy' if len(evaluation.triggered) == 1 else 'policies'} "
                f"triggered; the highest severity present determined the outcome."
            )

        if factors:
            leading = "; ".join(
                f"{f.note or f.factor} (weight {f.contribution:.2f})"
                for f in factors[:3]
            )
            parts.append(f"Leading factors: {leading}.")

        for outcome in evaluation.triggered:
            parts.append(
                f"[{outcome.policy_id} rev {outcome.policy_revision}] "
                f"{outcome.policy_title} - matched on {outcome.rationale}."
            )

        if evaluation.unevaluable:
            parts.append(
                "Policies that could not be evaluated because required signals "
                f"were absent: {', '.join(evaluation.unevaluable)}. "
                "Treat as unassessed, not as passed."
            )

        return " ".join(parts)
