# Governance Layer

Implements the parts of the Institutional Sovereignty Constitution that were
previously declared but not built.

| Module | Constitution article | What it does |
| :--- | :--- | :--- |
| `contracts/` | — | Shared types every other module depends on |
| `policies/` | Art. I, Art. IV | The rulebook, as data, plus the engine that evaluates it |
| `explainability/` | **Art. III** — Auditability & Explainability | Turns a decision into an auditable explanation |
| `oversight/` | **Art. V** — Human Oversight | The review queue that makes the kill-switch real |

## Why the rules moved out of the fraud engine

The overrides in `governance/controls/institutional_overrides.md` were
implemented as hardcoded branches inside `ai/fraud/engines/fraud_engine.py`.
That works, but it fails three tests any reviewer will apply:

- **Reviewability** — policy expressed as data can be read and challenged by
  someone who does not read Python. Policy buried in a scoring function cannot.
- **Traceability** — every policy now carries an id *and* a revision, so a
  finding can be traced to the exact rule version that produced it.
- **Changeability** — adding a rule means adding a registry entry, not editing
  a risk-scoring function and hoping nothing else moved.

`policy_registry.describe()` returns the entire rulebook as plain rows, with no
code in them. That is the artefact you hand an auditor.

## Three design decisions worth knowing

**1. Severity is an ordered enum, not a score.** A governance finding is a
classification. Averaging two findings is never meaningful, and an enum makes
that impossible by construction.

**2. Non-nettable findings force the outcome.** A `CRITICAL` result is not
diluted by favourable signals elsewhere. Some findings are disqualifying
regardless of the rest of the picture — and every other matching policy still
lands in the audit trail, because you cannot review a decision whose evidence
was discarded on the way.

**3. Missing evidence is not negative evidence.** A policy whose required
signal is absent is reported as `unevaluable`, never silently treated as
"did not match".

## Usage

```python
from governance.policies import PolicyEngine
from governance.explainability import ExplanationBuilder
from governance.oversight import ReviewQueue

signals = {"emulator_detected": True, "velocity_variance": 3.1}

evaluation  = PolicyEngine().evaluate(signals)
explanation = ExplanationBuilder().build("TXN-001", signals, evaluation, trace_id="t-1")
item        = ReviewQueue().submit("TXN-001", evaluation, explanation)

print(evaluation.overall_action)        # BLOCK
print(evaluation.non_nettable_override) # GOV-CTRL-FRAUD-001.1 is non-nettable...
print(explanation.narrative)
print(item.is_open)                     # True - a human must close it
```

Run `python -m governance.demo` for a full worked example.

## Tests

```bash
pytest governance/tests/ -q
```

21 offline tests. No database, no network, no API keys. Each asserts a
governance *rule* rather than an implementation detail, so the internals can be
refactored without rewriting the suite.

## Known limitations

- Factor weights in `explainability` are **documented, not learned**. They are
  stated plainly so a reviewer can challenge them; calibrating them against
  labelled outcomes is the obvious next step.
- The review queue persists to JSON. Fine for a single process; a real
  deployment needs the database and an access model behind it.
- There is no fairness or bias dimension yet. For any EU AI Act high-risk use
  case that is a material gap, not a nice-to-have.
