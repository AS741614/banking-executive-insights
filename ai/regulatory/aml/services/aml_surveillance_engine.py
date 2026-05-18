import logging
from datetime import datetime
from typing import List, Dict, Any, Tuple

from ai.regulatory.aml.models.aml_transaction_profile import (
    AMLTransactionProfile,
    TransactionLifecycleStatus
)

logger = logging.getLogger("esoteric_bank.compliance.aml_surveillance_engine")

class AMLSurveillanceEngine:
    """
    Institutional Banking Governance Infrastructure: AML Surveillance Cognition Engine.
    Executes transaction surveillance, suspicious activity detection, and SAR governance.
    """

    def __init__(self, governance_version: str = "v1.0.0"):
        self.governance_version = governance_version

    async def evaluate_transaction(
        self, profile: AMLTransactionProfile
    ) -> AMLTransactionProfile:
        """
        Executes an AML cognitive surveillance cycle on a single transaction.
        """
        logger.info(f"Initiating AML surveillance cycle for transaction: {profile.transaction_id}")

        # 1. Detect Suspicious Activity and Behavioral Risks
        suspicious_flags, behavioral_reasons = self._detect_suspicious_activity(profile)

        # 2. Analyze Structuring and Layering
        structural_severity, structural_reasons = self._analyze_structuring_layering(profile)

        # 3. Analyze Jurisdiction and Cross-Border Exposure
        jurisdiction_severity, jurisdiction_reasons = self._analyze_jurisdiction_exposure(profile)

        # 4. Calculate AML Severity and Governance Risk
        aml_severity, governance_risk_score, severity_reasons = self._calculate_overall_severity(
            profile, structural_severity, jurisdiction_severity, suspicious_flags
        )

        # 5. Determine Governance Escalation and SAR Recommendation
        requires_escalation, sar_recommended, escalation_reasons = self._determine_escalation(
            aml_severity, governance_risk_score, profile
        )

        # 6. Determine Transaction Lifecycle Status
        lifecycle_status, status_reasons = self._determine_lifecycle_status(
            profile, aml_severity, requires_escalation
        )

        # 7. Generate Governance Commentary
        all_reasons = (
            behavioral_reasons + structural_reasons + jurisdiction_reasons + 
            severity_reasons + escalation_reasons + status_reasons
        )
        commentary = self._generate_governance_commentary(all_reasons)

        # Update Profile State
        updated_profile = profile.model_copy(update={
            "suspicious_activity": profile.suspicious_activity.model_copy(update={
                "suspicious_activity_flag": suspicious_flags or profile.suspicious_activity.suspicious_activity_flag,
                "sar_filing_recommended": sar_recommended
            }),
            "risk_assessment": profile.risk_assessment.model_copy(update={
                "aml_severity": aml_severity,
                "governance_risk_score": governance_risk_score,
                "governance_escalation_flag": requires_escalation,
                "requires_manual_review": requires_escalation or sar_recommended
            }),
            "lifecycle_status": lifecycle_status
        })

        logger.info(
            f"AML surveillance cycle complete. Status: {lifecycle_status}, "
            f"Escalation: {requires_escalation}, SAR: {sar_recommended}"
        )
        
        # Attach the commentary to the logger or a separate persistence layer in reality
        logger.debug(f"Audit Reasoning: {commentary}")

        return updated_profile

    def _detect_suspicious_activity(self, profile: AMLTransactionProfile) -> Tuple[bool, List[str]]:
        reasons = []
        is_suspicious = False

        if profile.behavior_profile.anomaly_score > 0.8:
            is_suspicious = True
            reasons.append("HIGH RISK: Transaction anomaly score exceeds institutional threshold.")

        if profile.behavior_profile.behavioral_risk_score > 0.75:
            is_suspicious = True
            reasons.append("HIGH RISK: Behavioral risk profile indicates abnormal transaction patterns.")
            
        if profile.behavior_profile.velocity_score > 0.85:
            is_suspicious = True
            reasons.append("CRITICAL: High velocity of transactions detected in a short time window.")

        if profile.suspicious_activity.crypto_transaction_flag:
            reasons.append("INFO: Digital asset exposure detected, applying enhanced scrutiny.")

        return is_suspicious, reasons

    def _analyze_structuring_layering(self, profile: AMLTransactionProfile) -> Tuple[float, List[str]]:
        reasons = []
        severity = 0.0

        if profile.behavior_profile.structuring_score > 0.8:
            severity = max(severity, 0.9)
            reasons.append("CRITICAL: High probability of deposit structuring (smurfing) detected.")
        elif profile.behavior_profile.structuring_score > 0.6:
            severity = max(severity, 0.6)
            reasons.append("MEDIUM-HIGH: Potential structuring behavior observed.")

        if profile.behavior_profile.layering_score > 0.85:
            severity = max(severity, 0.95)
            reasons.append("CRITICAL: Complex layering behavior detected across multiple hops/accounts.")
            
        if profile.behavior_profile.cash_intensity_score > 0.7:
            severity = max(severity, 0.5)
            reasons.append("MEDIUM: Transaction exhibits high cash-intensity characteristics.")

        return severity, reasons

    def _analyze_jurisdiction_exposure(self, profile: AMLTransactionProfile) -> Tuple[float, List[str]]:
        reasons = []
        severity = 0.0

        if profile.jurisdiction_exposure.high_risk_jurisdiction_flag:
            severity = 0.85
            reasons.append(
                f"HIGH RISK: Transaction involves high-risk jurisdiction "
                f"({profile.jurisdiction_exposure.destination_country})."
            )

        if profile.jurisdiction_exposure.cross_border_flag and profile.transaction_amount > 50000:
            severity = max(severity, 0.6)
            reasons.append("MEDIUM-HIGH: Large value cross-border transaction.")

        return severity, reasons

    def _calculate_overall_severity(
        self, 
        profile: AMLTransactionProfile, 
        structural_severity: float, 
        jurisdiction_severity: float, 
        suspicious_flags: bool
    ) -> Tuple[float, float, List[str]]:
        reasons = []
        
        # Base severity composite
        aml_severity = max(
            profile.risk_assessment.aml_severity,
            structural_severity,
            jurisdiction_severity,
            profile.behavior_profile.anomaly_score
        )
        
        if suspicious_flags:
            aml_severity = max(aml_severity, 0.7)
            
        if profile.suspicious_activity.regulatory_watchlist_flag:
            aml_severity = 1.0
            reasons.append("CRITICAL: Counterparty or entity matches regulatory watchlist.")
            
        # Compute Governance Risk
        governance_risk_score = (aml_severity * 0.6) + (profile.behavior_profile.behavioral_risk_score * 0.4)
        
        return aml_severity, governance_risk_score, reasons

    def _determine_escalation(
        self, 
        aml_severity: float, 
        governance_risk: float, 
        profile: AMLTransactionProfile
    ) -> Tuple[bool, bool, List[str]]:
        reasons = []
        requires_escalation = False
        sar_recommended = False

        # --- HARDENED GOVERNANCE OVERRIDES ---
        
        # 1. Critical AML/Governance Thresholds
        if aml_severity >= 0.85 or governance_risk >= 0.8:
            requires_escalation = True
            reasons.append("ESOTERIC_HARD_OVERRIDE: AML Severity or Governance Risk exceeded critical institutional thresholds.")

        # 2. Digital Structuring & Mule Coordination (Hardened: No longer dependent on cash intensity)
        if profile.behavior_profile.structuring_score > 0.85:
            requires_escalation = True
            sar_recommended = True
            reasons.append("HARDENED_REASONING: High-confidence digital structuring/smurfing detected. Immediate SAR recommendation per institutional risk mandate.")

        # 3. Complex Layering Overrides
        if profile.behavior_profile.layering_score > 0.85:
            requires_escalation = True
            sar_recommended = True
            reasons.append("HARDENED_REASONING: Evident layering behavior identified. Circumvention of traditional monitoring thresholds suspected.")

        # 4. Regulatory Watchlist (Absolute Block)
        if profile.suspicious_activity.regulatory_watchlist_flag:
            requires_escalation = True
            sar_recommended = True
            reasons.append("CRITICAL_GOVERNANCE: Mandatory sanction/watchlist match detected. Immediate SAR and transaction hold mandatory.")

        # 5. Mule Account Indicators (Anomaly + High Velocity)
        if profile.behavior_profile.anomaly_score > 0.9 and profile.behavior_profile.velocity_score > 0.9:
            requires_escalation = True
            reasons.append("MULE_RISK_DETECTED: High-velocity anomalous coordination detected. Probable money mule activity.")

        return requires_escalation, sar_recommended, reasons

    def _determine_lifecycle_status(
        self, 
        profile: AMLTransactionProfile, 
        aml_severity: float, 
        requires_escalation: bool
    ) -> Tuple[TransactionLifecycleStatus, List[str]]:
        reasons = []

        if profile.suspicious_activity.regulatory_watchlist_flag:
            reasons.append("ACTION: Transaction HELD due to regulatory watchlist match.")
            return TransactionLifecycleStatus.HELD, reasons

        if requires_escalation:
            reasons.append("ACTION: Transaction ESCALATED to AML compliance team.")
            return TransactionLifecycleStatus.ESCALATED, reasons

        if aml_severity > 0.6:
            reasons.append("ACTION: Transaction PENDING secondary review.")
            return TransactionLifecycleStatus.PENDING, reasons

        reasons.append("ACTION: Transaction cleared for completion.")
        return TransactionLifecycleStatus.COMPLETED, reasons

    def _generate_governance_commentary(self, reasons: List[str]) -> str:
        if not reasons:
            return "No critical AML flags detected."
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        summary = " | ".join(reasons)
        return f"[{timestamp}] SURVEILLANCE_AUDIT: {summary}"

    def get_audit_trail(self, profile: AMLTransactionProfile, commentary: str) -> Dict[str, Any]:
        """
        Returns audit-ready compliance reasoning metadata for the given transaction profile.
        """
        return {
            "transaction_id": profile.transaction_id,
            "customer_id": profile.customer_id,
            "audit_id": profile.audit.audit_id,
            "lifecycle_status": profile.lifecycle_status,
            "aml_severity": profile.risk_assessment.aml_severity,
            "sar_recommended": profile.suspicious_activity.sar_filing_recommended,
            "governance_escalation": profile.risk_assessment.governance_escalation_flag,
            "surveillance_commentary": commentary,
            "timestamp": datetime.utcnow().isoformat()
        }