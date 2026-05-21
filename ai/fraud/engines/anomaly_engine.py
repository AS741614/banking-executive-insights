import logging
from typing import Dict, Any, List, Tuple
from ai.fraud.models.fraud_profile import BehavioralAnomalyProfile

logger = logging.getLogger("esoteric_bank.fraud.behavioral_anomaly")

class BehavioralAnomalyEngine:
    """
    Institutional Behavioral Anomaly Engine.
    Detects operational drift and unusual transaction patterns.
    """

    async def analyze_behavior(
        self, 
        customer_id: str, 
        current_activity: Dict[str, Any], 
        historical_baseline: Dict[str, Any]
    ) -> BehavioralAnomalyProfile:
        """
        Compares current activity against historical baseline to detect behavioral drift.
        """
        logger.info(f"Analyzing behavioral anomaly for customer: {customer_id}")
        
        # Calculate Variances (Institutional Logic)
        velocity_var = self._calculate_variance(
            current_activity.get("velocity", 0), 
            historical_baseline.get("avg_velocity", 1)
        )
        amount_var = self._calculate_variance(
            current_activity.get("amount", 0), 
            historical_baseline.get("avg_amount", 1)
        )
        
        geo_drift = current_activity.get("country") != historical_baseline.get("primary_country")
        unusual_time = self._check_time_anomaly(current_activity.get("hour", 0), historical_baseline.get("active_hours", []))

        # Compute Behavioral Risk Score
        risk_score = (velocity_var * 0.4) + (amount_var * 0.3)
        if geo_drift: risk_score += 0.2
        if unusual_time: risk_score += 0.1
        
        risk_score = min(1.0, risk_score)

        return BehavioralAnomalyProfile(
            velocity_variance=velocity_var,
            geographical_drift=geo_drift,
            unusual_time_pattern=unusual_time,
            amount_variance=amount_var,
            behavioral_risk_score=risk_score
        )

    def _calculate_variance(self, current: float, baseline: float) -> float:
        if baseline == 0: return 1.0
        return abs(current - baseline) / baseline

    def _check_time_anomaly(self, current_hour: int, active_hours: List[int]) -> bool:
        if not active_hours: return False
        return current_hour not in active_hours
