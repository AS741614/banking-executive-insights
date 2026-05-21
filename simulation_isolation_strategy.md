# ESOTERIC BANK: Simulation Isolation Strategy
**Audit ID**: SIM-ISO-20260518-001
**Status**: IMPLEMENTED
**Auditor**: Senior Institutional Simulation Governance Engineer

## 1. Isolation Architecture
To prevent synthetic crisis data from contaminating production certification logic, a strict **Cognitive Origin Isolation** framework has been implemented.

## 2. Structural Implementation
### 2.1 Origin Tagging
- **CognitiveOrigin Enum**: Introduced `PRODUCTION`, `SIMULATION`, and `REPLAY` as primary identifiers for all institutional state and tasks.
- **Model Hardening**: `CognitiveTask` and `InstitutionalState` now require an explicit `origin` tag (defaulting to `PRODUCTION`).

### 2.2 Registry Partitioning
- **Origin-Aware Storage**: The `InstitutionalStateRegistry` now stores state with mandatory origin attribution.
- **Audit Filtering**: `get_domain_state()` supports strict filtering by origin, allowing the audit engine to ignore `SIMULATION` data when calculating production stability.

## 3. Crisis Injection Isolation
- **Scenario Tagging**: `LiquidityDeteriorationScenario` and `FraudEscalationScenario` explicitly tag injected tasks as `SIMULATION`.
- **Runtime Propagation**: The `CognitiveRuntimeCoordinator` propagates the origin tag through the entire task lifecycle (QUEUED -> DISPATCHED).

## 4. Final Verification
- **Test Convergence**: Re-run of the convergence suite confirmed that `SIMULATION` tasks are correctly dispatched and tracked without impacting global `PRODUCTION` counters.

**Result**: SIMULATION_ISOLATION_SUCCESSFUL
