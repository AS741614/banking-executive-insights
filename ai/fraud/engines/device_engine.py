import logging
from typing import Dict, Any
from ai.fraud.models.fraud_profile import DeviceIntelligenceProfile

logger = logging.getLogger("esoteric_bank.fraud.device_intelligence")

class DeviceIntelligenceLayer:
    """
    Enterprise Device Intelligence Framework.
    Analyzes hardware and environment signals for fraud risk.
    """

    async def assess_device_risk(self, device_data: Dict[str, Any]) -> DeviceIntelligenceProfile:
        """
        Evaluates risk based on device fingerprint and network environment.
        """
        logger.info(f"Assessing device intelligence for ID: {device_data.get('device_id')}")

        vpn = device_data.get("vpn", False)
        proxy = device_data.get("proxy", False)
        tor = device_data.get("tor", False)
        emulator = device_data.get("emulator", False)
        velocity = device_data.get("device_velocity", 0)

        # Base Risk Calculation
        risk = 0.0
        if vpn: risk += 0.2
        if proxy: risk += 0.3
        if tor: risk += 0.5
        if emulator: risk += 0.6
        if velocity > 5: risk += 0.4
        
        risk = min(1.0, risk)

        return DeviceIntelligenceProfile(
            device_id=device_data.get("device_id", "UNKNOWN"),
            ip_address=device_data.get("ip", "0.0.0.0"),
            vpn_detected=vpn,
            proxy_detected=proxy,
            tor_detected=tor,
            emulator_detected=emulator,
            location_country=device_data.get("country", "UNKNOWN"),
            velocity_count=velocity,
            risk_score=risk
        )
