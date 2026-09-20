"""Offline tests for the governance layer.

No database, no network, no API keys - these run anywhere, which is the point.
Each test asserts a governance *rule*, not an implementation detail, so the
internals can be refactored without rewriting the suite.
"""
from __future__ import annotations

import pytest

from governance.contracts import (
    GovernanceAction,
    ReviewDecision,
    Severity,
)
from governance.explainability import ExplanationBuilder
from governance.oversight import ReviewQueue, ReviewQueueError
from governance.policies import PolicyEngine, describe, registry


# --- severity ---------------------------------------------------------------

def test_severity_is_ordered_not_alphabetical():
    assert Severity.rank(Severity.CRITICAL) > Severity.rank(Severity.HIGH)
    assert Severity.rank(Severity.LOW) > Severity.rank(Severity.INFORMATIONAL)


def test_highest_severity_wins():
    assert Severity.highest([Severity.LOW, Severity.CRITICAL, Severity.MEDIUM]) == Severity.CRITICAL


def test_highest_of_nothing_is_informational():
    assert Severity.highest([]) == Severity.INFORMATIONAL


# --- policy registry --------------------------------------------------------

def test_registry_is_not_empty_and_ids_are_unique():
    ids = [p.policy_id for p in registry()]
    assert ids
    assert len(ids) == len(set(ids))


def test_every_policy_carries_a_revision_and_an_article_reference():
    for policy in registry():
        assert policy.revision, f"{policy.policy_id} has no revision"
        assert policy.article_ref, f"{policy.policy_id} has no article reference"


def test_describe_is_code_free_and_covers_every_policy():
    rows = describe()
    assert len(rows) == len(registry())
    for row in rows:
        assert set(row).issuperset({"policy_id", "condition", "severity", "action"})


# --- policy engine ----------------------------------------------------------

def test_clean_signals_trigger_nothing():
    result = PolicyEngine().evaluate({"vpn_risk_score": 0.1, "velocity_variance": 0.2})
    assert result.triggered == []
    assert result.overall_action == GovernanceAction.MONITOR
    assert result.overall_severity == Severity.INFORMATIONAL


def test_emulator_forces_a_block():
    result = PolicyEngine().evaluate({"emulator_detected": True})
    assert result.overall_action == GovernanceAction.BLOCK
    assert result.overall_severity == Severity.CRITICAL


def test_non_nettable_finding_is_not_diluted_by_favourable_signals():
    """The whole point: a critical finding cannot be averaged away."""
    result = PolicyEngine().evaluate(
        {
            "emulator_detected": True,   # non-nettable CRITICAL
            "vpn_risk_score": 0.0,       # everything else is clean
            "velocity_variance": 0.0,
            "structuring_score": 0.0,
        }
    )
    assert result.overall_severity == Severity.CRITICAL
    assert result.non_nettable_override is not None
    assert "GOV-CTRL-FRAUD-001.1" in result.non_nettable_override


def test_every_matching_policy_is_recorded_not_just_the_worst():
    result = PolicyEngine().evaluate(
        {
            "tor_detected": True,        # CRITICAL
            "vpn_risk_score": 0.95,      # HIGH
            "layering_score": 0.9,       # HIGH
        }
    )
    ids = {o.policy_id for o in result.triggered}
    assert len(ids) == 3, "lower-severity findings must survive in the audit trail"


def test_impossible_travel_needs_both_conditions():
    only_drift = PolicyEngine().evaluate(
        {"geographical_drift": True, "velocity_variance": 0.5}
    )
    assert all(o.policy_id != "GOV-CTRL-FRAUD-001.4" for o in only_drift.triggered)

    both = PolicyEngine().evaluate(
        {"geographical_drift": True, "velocity_variance": 2.5}
    )
    assert any(o.policy_id == "GOV-CTRL-FRAUD-001.4" for o in both.triggered)


def test_strictest_action_wins_when_nothing_is_non_nettable():
    result = PolicyEngine().evaluate({"layering_score": 0.9})  # ESCALATE, nettable
    assert result.overall_action == GovernanceAction.ESCALATE
    assert result.non_nettable_override is None


# --- explainability ---------------------------------------------------------

def test_explanation_cites_policies_with_their_revision():
    signals = {"emulator_detected": True}
    evaluation = PolicyEngine().evaluate(signals)
    record = ExplanationBuilder().build("TXN-1", signals, evaluation, trace_id="trace-1")

    assert record.policies_applied
    assert all("@" in ref for ref in record.policies_applied), "revision must be cited"
    assert record.trace_id == "trace-1"


def test_explanation_lists_factors_in_order_of_contribution():
    signals = {"emulator_detected": True, "unusual_time_pattern": True}
    evaluation = PolicyEngine().evaluate(signals)
    record = ExplanationBuilder().build("TXN-2", signals, evaluation)

    contributions = [f.contribution for f in record.factors]
    assert contributions == sorted(contributions, reverse=True)
    assert record.top_factors(1)[0].factor == "emulator_detected"


def test_clean_decision_still_produces_an_explanation():
    signals = {"vpn_risk_score": 0.0}
    evaluation = PolicyEngine().evaluate(signals)
    record = ExplanationBuilder().build("TXN-3", signals, evaluation)
    assert record.narrative
    assert record.decision == GovernanceAction.MONITOR


# --- oversight --------------------------------------------------------------

def test_low_severity_does_not_require_human_review():
    queue = ReviewQueue()
    evaluation = PolicyEngine().evaluate({"vpn_risk_score": 0.0})
    assert queue.submit("TXN-4", evaluation) is None


def test_critical_finding_is_queued_for_a_human():
    queue = ReviewQueue()
    evaluation = PolicyEngine().evaluate({"emulator_detected": True})
    item = queue.submit("TXN-5", evaluation)

    assert item is not None
    assert item.is_open
    assert queue.summary()["critical_open"] == 1


def test_a_decision_without_a_rationale_is_refused():
    """Rule 2: a verdict with no reviewer or reason is not an audit trail."""
    queue = ReviewQueue()
    item = queue.submit("TXN-6", PolicyEngine().evaluate({"tor_detected": True}))

    with pytest.raises(ReviewQueueError):
        queue.record_decision(item.item_id, ReviewDecision.UPHELD, "", "")


def test_an_item_cannot_be_silently_decided_twice():
    queue = ReviewQueue()
    item = queue.submit("TXN-7", PolicyEngine().evaluate({"tor_detected": True}))
    queue.record_decision(item.item_id, ReviewDecision.UPHELD, "a.sharma", "Confirmed.")

    with pytest.raises(ReviewQueueError):
        queue.record_decision(
            item.item_id, ReviewDecision.OVERTURNED, "a.sharma", "Changed my mind."
        )


def test_override_rate_tracks_human_reversals():
    queue = ReviewQueue()
    upheld = queue.submit("TXN-8", PolicyEngine().evaluate({"tor_detected": True}))
    overturned = queue.submit("TXN-9", PolicyEngine().evaluate({"emulator_detected": True}))

    queue.record_decision(upheld.item_id, ReviewDecision.UPHELD, "a.sharma", "Correct.")
    queue.record_decision(
        overturned.item_id, ReviewDecision.OVERTURNED, "a.sharma", "False positive."
    )

    assert queue.override_rate() == 0.5


def test_queue_survives_a_restart(tmp_path):
    store = tmp_path / "oversight.json"
    first = ReviewQueue(store_path=store)
    item = first.submit("TXN-10", PolicyEngine().evaluate({"emulator_detected": True}))

    reloaded = ReviewQueue(store_path=store)
    assert reloaded.get(item.item_id) is not None
    assert reloaded.get(item.item_id).is_open
