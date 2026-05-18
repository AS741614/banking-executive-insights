# ESOTERIC BANK: Certification Filtering Rules
**Audit ID**: CERT-FILT-20260518-001
**Status**: ACTIVE
**Auditor**: Enterprise Certification Auditor

## 1. Audit Filtering Mandate
Institutional audits must distinguish between controlled synthetic stress and genuine production instability. The following rules define the filtering logic for all certification cycles.

## 2. Filtering Logic Table
| Data Type | Origin Filter | Certification Treatment |
| :--- | :--- | :--- |
| **Liquidity Drifts** | `PRODUCTION` | **BLOCKER** if below $100k threshold. |
| **Liquidity Drifts** | `SIMULATION` | **IGNORE** (Validate response only). |
| **Fraud Events** | `PRODUCTION` | **ESCALATE** for immediate manual review. |
| **Fraud Events** | `SIMULATION` | **TRACK** for orchestration performance validation. |
| **Service Latency** | `PRODUCTION` | **FAIL** if > 500ms P99. |
| **Service Latency** | `SIMULATION` | **REPORT** for resource contention analysis. |

## 3. Exclusion Rules
1. **Rule_SIM_001**: Any `InstitutionalState` with `origin=SIMULATION` must be excluded from the "Production Health Snapshot."
2. **Rule_SIM_002**: `SIMULATION` tasks that result in `DISPATCHED` status do NOT count toward production "Active Incident" quotas.
3. **Rule_SIM_003**: Telemetry labeled with `CognitiveOrigin.SIMULATION` is filtered from executive-grade compliance reporting.

## 4. Auditor Certification
Filtering rules have been calibrated to ensure zero leakage of synthetic crisis data into the production governance layer.
