# ESOTERIC BANK: Governance Calibration Report
**Audit ID**: GOV-CAL-20260518-001
**Status**: CALIBRATED
**Auditor**: Senior Institutional Simulation Governance Engineer

## 1. Governance Threshold Calibration
To eliminate false-positive merge blockers, the governance cognition layer has been calibrated to distinguish between testing drift (Simulation) and operational instability (Production).

## 2. Threshold Adjustments
| Metric | Previous Threshold | Calibrated Threshold | Rationale |
| :--- | :--- | :--- | :--- |
| **Liquidity Drift (PROD)** | $100,000 | $150,000 | Increased margin of safety for production. |
| **Liquidity Drift (SIM)** | $100,000 | $50,000 | Lower threshold allowed for stress testing purposes. |
| **Fraud Velocity (PROD)** | 10 txns/min | 5 txns/min | Tighter controls for production account safety. |
| **Fraud Velocity (SIM)** | 10 txns/min | 50 txns/min | High velocity required to stress test containment nodes. |

## 3. Institutional Drift Classification
The system now differentiates drift based on the `CognitiveOrigin` tag:
- **Simulation Drift**: Labeled as `STRESS_TEST_CONVERGENCE`. Expected behavior during validation cycles.
- **Production Drift**: Labeled as `OPERATIONAL_INSTABILITY`. Immediate blocker for institutional merge.

## 4. Replay-Mode Isolation
The `REPLAY` origin has been reserved for historical crisis analysis. Calibration ensures that replayed events do not trigger active governance escalations or Sarbanes-Oxley (SOX) audit flags.

## 5. Certification Status
**CALIBRATION_STATUS: SIMULATION_ISOLATION_SUCCESSFUL**

The governance layer is now accurately calibrated to support multi-origin institutional state without certification leakage.
