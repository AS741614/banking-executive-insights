import logging
import uuid
from datetime import datetime
from typing import Dict, Any, List, Tuple

from ai.fraud.models.fraud_profile import (
    FraudIntelligenceProfile, 
    FraudRiskLevel, 
    DeviceIntelligenceProfile, 
    BehavioralAnomalyProfile
)
from ai.fraud.engines.anomaly_engine import BehavioralAnomalyEngine
from ai.fraud.engines.device_engine import DeviceIntelligenceLayer

logger = logging.getLogger("esoteric_bank.fraud.detection_engine")

class FraudDetectionEngine:
    """
    Enterprise Fraud Detection Engine.
    Synthesizes behavioral and device intelligence into institutional fraud cognition.
    """

    def __init__(self):
        self.anomaly_engine = BehavioralAnomalyEngine()
        self.device_layer = DeviceIntelligenceLayer()

    async def execute_fraud_cognition(
        self, 
        customer_id: str, 
        transaction_data: Dict[str, Any],
        historical_context: Dict[str, Any]
    ) -> FraudIntelligenceProfile:
        """
        Main cognition cycle for fraud detection.
        """
        logger.info(f"Executing fraud cognition cycle for customer: {customer_id}")

        # 1. Device Intelligence
        device_profile = await self.device_layer.assess_device_risk(transaction_data.get("device_context", {}))

        # 2. Behavioral Anomaly
        behavior_profile = await self.anomaly_engine.analyze_behavior(
            customer_id, 
            transaction_data, 
            historical_context
        )

        # 3. Composite Scoring & Pattern Matching
        composite_score, patterns = self._calculate_composite_score(device_profile, behavior_profile)
        
        # 4. Classify Risk Level
        risk_level = self._classify_risk_level(composite_score)

        # 5. Synthetic Identity & ATO Analysis
        is_synthetic = self._check_synthetic_identity(transaction_data, behavior_profile)
        ato_prob = self._calculate_ato_probability(device_profile, behavior_profile)

        # 6. Determine Governance Action
        action, commentary = self._determine_governance(risk_level, patterns, ato_prob)

        return FraudIntelligenceProfile(
            fraud_assessment_id=f"FRAUD-{uuid.uuid4().hex[:8].upper()}",
            customer_id=customer_id,
            transaction_id=transaction_data.get("transaction_id"),
            risk_level=risk_level,
            composite_fraud_score=composite_score,
            device_intelligence=device_profile,
            behavioral_anomaly=behavior_profile,
            detected_patterns=patterns,
            is_synthetic_identity_suspected=is_synthetic,
            account_takeover_probability=ato_prob,
            governance_action=action,
            governance_commentary=commentary
        )

    def _calculate_composite_score(
        self, 
        device: DeviceIntelligenceProfile, 
        behavior: BehavioralAnomalyProfile
    ) -> Tuple[float, List[str]]:
        patterns = []
        
        # --- HARDENED RISK OVERRIDES (Eliminating Dilution) ---
        
        # 1. Emulator Detection Override (Absolute Critical Threat)
        if device.emulator_detected:
            patterns.append("CRITICAL_THREAT: EMULATOR_DETECTED")
            return 1.0, patterns

        # 2. Impossible Travel Override (Geo Drift + Velocity Variance)
        if behavior.geographical_drift and behavior.velocity_variance > 1.5:
            patterns.append("CRITICAL_THREAT: IMPOSSIBLE_TRAVEL_PATTERN")
            return 0.98, patterns

        # 3. High Risk Network Override (Tor/Proxy + Anomaly)
        if (device.tor_detected or device.proxy_detected) and behavior.behavioral_risk_score > 0.7:
            patterns.append("HIGH_THREAT: ANONYMIZED_NETWORK_WITH_ANOMALY")
            return 0.90, patterns

        # Standard weighted calculation if no overrides triggered
        score = (device.risk_score * 0.6) + (behavior.behavioral_risk_score * 0.4)
        
        if behavior.velocity_variance > 2.0:
            patterns.append("PATTERN: HIGH_VELOCITY_BURST")
            score = max(score, 0.75)

        return min(1.0, score), patterns

    def _classify_risk_level(self, score: float) -> FraudRiskLevel:
        if score >= 0.90: return FraudRiskLevel.CRITICAL
        if score >= 0.70: return FraudRiskLevel.HIGH
        if score >= 0.45: return FraudRiskLevel.MEDIUM
        if score >= 0.25: return FraudRiskLevel.LOW
        return FraudRiskLevel.NEGLEGIBLE

    def _check_synthetic_identity(self, data: Dict[str, Any], behavior: BehavioralAnomalyProfile) -> bool:
        # Synthetic identities often have "perfect" start but unusual depth patterns
        return data.get("identity_age_days", 365) < 30 and behavior.amount_variance > 5.0

    def _calculate_ato_probability(self, device: DeviceIntelligenceProfile, behavior: BehavioralAnomalyProfile) -> float:
        # Harden ATO calculation to prioritize device risk
        if device.risk_score > 0.8: return 1.0
        prob = (device.risk_score * 0.75) + (behavior.geographical_drift * 0.25)
        return min(1.0, prob)

    def _determine_governance(self, risk: FraudRiskLevel, patterns: List[str], ato: float) -> Tuple[str, str]:
        # Absolute Blocks
        if "CRITICAL_THREAT: EMULATOR_DETECTED" in patterns:
            return "BLOCK", "MANDATORY_BLOCK: Emulator session detected. Verification failed."
            
        if risk == FraudRiskLevel.CRITICAL or ato > 0.9:
            return "BLOCK", f"Institutional risk threshold exceeded. Patterns: {', '.join(patterns)}. High ATO probability."
        
        if risk == FraudRiskLevel.HIGH:
            return "CHALLENGE", "Elevated risk markers detected. Step-up authentication required."
            
        return "MONITOR", "Standard behavioral monitoring active."
