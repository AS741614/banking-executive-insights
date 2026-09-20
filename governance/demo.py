"""Worked example: signals -> policy -> explanation -> human review.

Run with:  python -m governance.demo
"""
from __future__ import annotations

from governance.contracts import ReviewDecision
from governance.explainability import ExplanationBuilder
from governance.oversight import ReviewQueue
from governance.policies import PolicyEngine, describe


def main() -> None:
    print("=" * 74)
    print("THE RULEBOOK")
    print("=" * 74)
    for row in describe():
        flag = " [non-nettable]" if row["non_nettable"] == "yes" else ""
        print(f"  {row['policy_id']:<24} {row['severity']:<13} {row['action']:<10}{flag}")
        print(f"  {'':<24} when: {row['condition']}")

    # A transaction that looks fine on almost every axis, with one hard failure.
    signals = {
        "emulator_detected": True,
        "vpn_risk_score": 0.05,
        "velocity_variance": 0.1,
        "structuring_score": 0.0,
        "unusual_time_pattern": True,
    }

    print()
    print("=" * 74)
    print("EVALUATION")
    print("=" * 74)
    evaluation = PolicyEngine().evaluate(signals)
    print(f"  Severity : {evaluation.overall_severity}")
    print(f"  Action   : {evaluation.overall_action}")
    print(f"  Override : {evaluation.non_nettable_override or 'none'}")
    print(f"  Triggered: {[o.policy_id for o in evaluation.triggered]}")

    print()
    print("=" * 74)
    print("EXPLANATION  (Constitution Art. III)")
    print("=" * 74)
    explanation = ExplanationBuilder().build(
        "TXN-DEMO-001", signals, evaluation, trace_id="trace-demo-001"
    )
    print(f"  {explanation.narrative}")
    print()
    print("  Top factors:")
    for factor in explanation.top_factors():
        print(f"    - {factor.factor:<24} {factor.contribution:.2f}  {factor.note}")
    print(f"  Policies applied: {explanation.policies_applied}")

    print()
    print("=" * 74)
    print("HUMAN OVERSIGHT  (Constitution Art. V)")
    print("=" * 74)
    queue = ReviewQueue()
    item = queue.submit("TXN-DEMO-001", evaluation, explanation)
    print(f"  Raised   : {item.item_id} ({item.severity})")
    print(f"  Open     : {item.is_open}  <- cannot close itself")

    queue.record_decision(
        item.item_id,
        ReviewDecision.UPHELD,
        reviewer="a.sharma",
        rationale="Emulator signal confirmed against device telemetry.",
    )
    print(f"  Decision : {item.decision} by {item.reviewer}")
    print(f"  Rationale: {item.reviewer_rationale}")
    print(f"  Summary  : {queue.summary()}")


if __name__ == "__main__":
    main()
