import logging
from datetime import datetime
from typing import List, Dict, Any, Tuple

from ai.regulatory.kyc.models.customer_profile import (
    CustomerKYCCognitionProfile,
    ComplianceStatus,
    GovernanceTier,
    LifecycleStatus,
    GovernanceAuditMetadata
)

logger = logging.getLogger("esoteric_bank.compliance.kyc_risk_engine")

class KYCRiskCognitionEngine:
    """
    Institutional Banking Governance Infrastructure: KYC Risk Cognition Engine.
    Performs dynamic risk scoring, governance tiering, and compliance escalation.
    """

    def __init__(self, governance_version: str = "v1.0.0"):
        self.governance_version = governance_version

    async def evaluate_customer_profile(
        self, profile: CustomerKYCCognitionProfile
    ) -> CustomerKYCCognitionProfile:
        """
        Executes a full cognitive risk assessment cycle on a customer profile.
        """
        logger.info(f"Initiating risk cognition cycle for customer: {profile.identity.customer_id}")

        # 1. Evaluate AML and Exposure Severity
        aml_severity, exposure_reasons = self._calculate_aml_severity(profile)

        # 2. Determine Governance Tier
        governance_tier, tier_reasons = self._determine_governance_tier(profile, aml_severity)

        # 3. Assess EDD Escalation Requirements
        edd_escalated, edd_reasons = self._assess_edd_requirement(profile, aml_severity, governance_tier)

        # 4. Determine Compliance Status
        compliance_status, status_reasons = self._determine_compliance_status(
            profile, aml_severity, edd_escalated
        )

        # 5. Generate Governance Commentary
        commentary = self._generate_governance_commentary(
            exposure_reasons + tier_reasons + edd_reasons + status_reasons
        )

        # Update Profile State
        updated_profile = profile.model_copy(update={
            "compliance_status": compliance_status,
            "governance_tier": governance_tier,
            "edd_profile": profile.edd_profile.model_copy(update={
                "edd_required": edd_escalated,
                "investigation_notes": profile.edd_profile.investigation_notes + [commentary]
            })
        })

        logger.info(f"Risk cognition cycle complete. Status: {compliance_status}, Tier: {governance_tier}")
        return updated_profile

    def _calculate_aml_severity(self, profile: CustomerKYCCognitionProfile) -> Tuple[float, List[str]]:
        reasons = []
        severity = profile.risk_assessment.aml_risk_score

        if profile.exposure.sanction_flag:
            severity = 1.0
            reasons.append("CRITICAL: Sanction list match detected.")
        
        if profile.exposure.pep_flag:
            severity = max(severity, 0.8)
            reasons.append("HIGH: Politically Exposed Person (PEP) status identified.")

        if profile.exposure.adverse_media_flag:
            severity = max(severity, 0.7)
            reasons.append("MEDIUM-HIGH: Adverse media presence detected.")

        if profile.jurisdiction.is_high_risk:
            severity = max(severity, 0.75)
            reasons.append(f"HIGH: Jurisdiction {profile.jurisdiction.jurisdiction_code} is classified as high-risk.")

        if profile.exposure.crypto_exposure:
            severity = max(severity, 0.6)
            reasons.append("MEDIUM: Digital asset/crypto exposure identified.")

        return severity, reasons

    def _determine_governance_tier(
        self, profile: CustomerKYCCognitionProfile, aml_severity: float
    ) -> Tuple[GovernanceTier, List[str]]:
        reasons = []
        
        if aml_severity >= 0.9 or profile.exposure.sanction_flag:
            reasons.append("Escalating to RESTRICTED tier due to critical AML exposure.")
            return GovernanceTier.TIER_3_RESTRICTED, reasons
        
        if aml_severity >= 0.6 or profile.risk_assessment.annual_income > 1000000:
            reasons.append("Escalating to ENHANCED tier based on risk profile and wealth markers.")
            return GovernanceTier.TIER_2_ENHANCED, reasons

        return GovernanceTier.TIER_1_STANDARD, ["Standard governance tier applied."]

    def _assess_edd_requirement(
        self, 
        profile: CustomerKYCCognitionProfile, 
        aml_severity: float, 
        tier: GovernanceTier
    ) -> Tuple[bool, List[str]]:
        reasons = []
        requires_edd = False

        if aml_severity > 0.7:
            requires_edd = True
            reasons.append("EDD triggered by high AML severity score.")
        
        if tier == GovernanceTier.TIER_3_RESTRICTED:
            requires_edd = True
            reasons.append("EDD mandatory for Restricted governance tier.")

        if profile.risk_assessment.onboarding_risk_score > 0.8:
            requires_edd = True
            reasons.append("EDD triggered by high onboarding risk variance.")

        return requires_edd, reasons

    def _determine_compliance_status(
        self, 
        profile: CustomerKYCCognitionProfile, 
        aml_severity: float, 
        edd_escalated: bool
    ) -> Tuple[ComplianceStatus, List[str]]:
        reasons = []
        
        if profile.exposure.sanction_flag:
            reasons.append("Compliance REJECTED: Mandatory sanction block.")
            return ComplianceStatus.REJECTED, reasons
        
        if aml_severity > 0.8 or edd_escalated:
            reasons.append("Compliance UNDER_REVIEW: High risk markers require manual intervention.")
            return ComplianceStatus.UNDER_REVIEW, reasons

        if aml_severity < 0.4 and not edd_escalated:
            reasons.append("Compliance APPROVED: Low risk profile verified.")
            return ComplianceStatus.APPROVED, reasons

        return ComplianceStatus.PENDING, ["Awaiting final governance validation."]

    def _generate_governance_commentary(self, reasons: List[str]) -> str:
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        summary = " | ".join(reasons)
        return f"[{timestamp}] GOVERNANCE_REASONING: {summary}"

    def get_audit_trail(self, profile: CustomerKYCCognitionProfile) -> Dict[str, Any]:
        """
        Returns audit-ready reasoning metadata for the given profile.
        """
        return {
            "customer_id": profile.identity.customer_id,
            "audit_id": profile.audit.audit_id,
            "compliance_status": profile.compliance_status,
            "governance_tier": profile.governance_tier,
            "composite_risk_score": profile.risk_assessment.composite_risk_score,
            "governance_notes": profile.edd_profile.investigation_notes,
            "timestamp": datetime.utcnow().isoformat()
        }
