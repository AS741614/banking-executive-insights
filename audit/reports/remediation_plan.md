# ESOTERIC BANK: Governance Remediation Plan
**Status**: DRAFT FOR EXECUTIVE APPROVAL
**Target Implementation**: Q3 2026

## 1. AML Workflow Remediation

### 1.1. Decouple Structuring from Cash Intensity
- **Issue**: SAR recommendations for structuring currently require high cash intensity.
- **Remediation**: Update `AMLSurveillanceEngine._determine_escalation` to trigger SAR recommendations based on `structuring_score` alone if it exceeds 0.9, or in combination with high `layering_score`.
- **Target Logic**:
  ```python
  if profile.behavior_profile.structuring_score > 0.9:
      sar_recommended = True
  ```

### 1.2. Harden SAR Recommendations
- **Remediation**: Ensure any `regulatory_watchlist_flag` match automatically triggers both `requires_escalation` and `sar_recommended`.

## 2. Fraud Governance Remediation

### 2.1. Escalation Threshold Adjustment
- **Issue**: Emulator detection (0.6 risk) is diluted by neutral behavioral signals.
- **Remediation**: Implement a "Critical Signal Override" in `FraudDetectionEngine`. If certain device signals (Emulator, TOR, high-velocity IP) are detected, the `risk_level` should be floor-rated at HIGH regardless of behavioral score.
- **Target Logic**:
  ```python
  if device_profile.emulator_detected or device_profile.tor_detected:
      risk_level = max(risk_level, FraudRiskLevel.HIGH)
  ```

### 2.2. Behavioral Context Enhancement
- **Remediation**: Enhance `BehavioralAnomalyEngine` to flag "New Device on Established Account" as a high-risk factor to complement device intelligence.

## 3. Governance Sovereignty and Observability

### 3.1. Centralized Policy Management
- **Remediation**: Move the `_policy_registry` from `GovernanceContinuityLayer` to a persistent configuration service (e.g., HashiCorp Vault or a dedicated DB table) to allow for dynamic, audited policy updates.

### 3.2. Automated Drift Remediation
- **Remediation**: Extend `governance_drift_detector.py` to not only report drift but also trigger automated "governance freezes" on affected regions or segments when CRITICAL drift is detected.

## 4. Next Steps
1. Review and approve remediation plan by the Governance Board.
2. Implement logic changes in `ai/regulatory/aml` and `ai/fraud`.
3. Re-run `audit/workflow_validation_framework.py` to verify pass rates.
