import logging
from ai.observability.core.config import obs_settings
from ai.events.engines.event_bus import event_bus

logger = logging.getLogger("esoteric_bank.observability.startup")

def validate_observability_subsystem():
    """
    Validates that the institutional observability sub-system is ready for local deployment.
    """
    print("--- ESOTERIC Observability: Startup Validation ---")
    
    # 1. Validate Config
    if not obs_settings.INSTITUTIONAL_BASELINES:
        print("[FAIL] Institutional baselines missing.")
        return False
    print("[OK] Telemetry baselines initialized.")
    
    # 2. Validate Event Bus
    if not event_bus:
        print("[FAIL] Event bus singleton not initialized.")
        return False
    print("[OK] Cognitive event bus active.")
    
    # 3. Validate Structured Logging
    try:
        from ai.observability.core.logging import structured_logger
        structured_logger.info("Observability startup validation in progress.")
        print("[OK] Structured JSON logging active.")
    except Exception as e:
        print(f"[FAIL] Structured logging initialization failed: {e}")
        return False

    print("\n[SUCCESS] Observability sub-system stabilized and ready.")
    return True

if __name__ == "__main__":
    validate_observability_subsystem()
