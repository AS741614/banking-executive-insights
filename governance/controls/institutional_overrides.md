# Institutional Governance Controls: Risk Overrides
**Policy ID**: GOV-CTRL-FRAUD-001
**Revision**: 1.1 (2026-05-18)

## 1. Critical Hardware Threat Overrides
The following hardware signals trigger an immediate **Institutional Override**, forcing a `CRITICAL` risk classification and an absolute `BLOCK` on the transaction.

| Threat Type | Signal Source | Governance Action |
| :--- | :--- | :--- |
| **Emulator Detected** | `device_intelligence.emulator_detected` | **MANDATORY_BLOCK** |
| **TOR Node** | `device_intelligence.tor_detected` | **MANDATORY_BLOCK** |
| **High-Risk VPN** | `device_intelligence.vpn_risk_score > 0.9` | **CHALLENGE (MFA)** |
| **Impossible Travel** | `behavioral_anomaly.geographical_drift` AND `velocity_variance > 2.0` | **MANDATORY_BLOCK** |

## 2. AML Compliance Overrides
The following compliance signals trigger an immediate **Regulatory Escalation**, forcing a `HELD` status and a `SAR_RECOMMENDED` flag.

| Compliance Type | Trigger | Governance Action |
| :--- | :--- | :--- |
| **Watchlist Match** | `suspicious_activity.regulatory_watchlist_flag` | **HELD / SAR_RECOMMENDED** |
| **Digital Structuring** | `behavior_profile.structuring_score > 0.9` | **ESCALATED / SAR_RECOMMENDED** |
| **Layering Pattern** | `behavior_profile.layering_score > 0.85` | **ESCALATED** |

## 3. Override Logging
All overrides must be logged with the `ESOTERIC_HARD_OVERRIDE` tag and include the raw hardware/compliance signal that triggered the override.
