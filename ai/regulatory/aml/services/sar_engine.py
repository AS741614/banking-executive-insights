import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

from ai.regulatory.aml.models.aml_transaction_profile import AMLTransactionProfile
from ai.regulatory.fraud.models.fraud_profile import FraudIntelligenceProfile

logger = logging.getLogger("esoteric_bank.compliance.sar_engine")

class SARRecommendation(BaseModel):
    recommendation_id: str
    customer_id: str
    case_type: str  # AML, FRAUD, HYBRID
    priority: str
    reasoning_summary: str
    involved_transaction_ids: List[str]
    suggested_narrative: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class SARRecommendationEngine:
    """
    Institutional SAR (Suspicious Activity Report) Recommendation Engine.
    Automates the generation of regulatory reporting logic.
    """

    def __init__(self, governance_version: str = "v1.0.0"):
        self.governance_version = governance_version

    async def generate_recommendation(
        self, 
        aml_profile: Optional[AMLTransactionProfile] = None,
        fraud_profile: Optional[FraudIntelligenceProfile] = None
    ) -> SARRecommendation:
        """
        Synthesizes AML and Fraud cognition into a structured SAR recommendation.
        """
        logger.info("Synthesizing SAR recommendation from multi-domain cognition.")
        
        customer_id = aml_profile.customer_id if aml_profile else fraud_profile.customer_id
        involved_txs = [aml_profile.transaction_id] if aml_profile and aml_profile.transaction_id else []
        if fraud_profile and fraud_profile.transaction_id:
            involved_txs.append(fraud_profile.transaction_id)

        case_type = self._determine_case_type(aml_profile, fraud_profile)
        priority = self._determine_priority(aml_profile, fraud_profile)
        narrative = self._generate_regulatory_narrative(aml_profile, fraud_profile)

        recommendation = SARRecommendation(
            recommendation_id=f"SAR-REC-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            customer_id=customer_id,
            case_type=case_type,
            priority=priority,
            reasoning_summary=f"Automated synthesis of {case_type} cognition.",
            involved_transaction_ids=involved_txs,
            suggested_narrative=narrative
        )

        logger.info(f"SAR recommendation generated: {recommendation.recommendation_id} (Priority: {priority})")
        return recommendation

    def _determine_case_type(self, aml: Optional[AMLTransactionProfile], fraud: Optional[FraudIntelligenceProfile]) -> str:
        if aml and fraud: return "HYBRID"
        if aml: return "AML"
        return "FRAUD"

    def _determine_priority(self, aml: Optional[AMLTransactionProfile], fraud: Optional[FraudIntelligenceProfile]) -> str:
        score = 0
        if aml and aml.risk_assessment.aml_severity > 0.8: score += 2
        if fraud and fraud.confidence_score > 0.8: score += 2
        
        if score >= 3: return "URGENT"
        if score >= 1: return "HIGH"
        return "STANDARD"

    def _generate_regulatory_narrative(self, aml: Optional[AMLTransactionProfile], fraud: Optional[FraudIntelligenceProfile]) -> str:
        parts = ["Institutional Regulatory Narrative:"]
        if aml:
            parts.append(f"AML Surveillance detected severity {aml.risk_assessment.aml_severity}.")
        if fraud:
            parts.append(f"Fraud Intelligence identified {fraud.fraud_type} with {fraud.confidence_score} confidence.")
        return " ".join(parts)
