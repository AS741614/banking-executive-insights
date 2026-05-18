import os
import sys
import logging
from typing import List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("infra.config.validator")

class ConfigValidator:
    """
    Validates the enterprise runtime environment and security configurations.
    """
    
    REQUIRED_VARS = [
        "SECRET_KEY",
        "DATABASE_URL",
        "ENVIRONMENT"
    ]
    
    INSECURE_DEFAULTS = [
        "ESOTERIC-SUPER-SECRET-GOVERNANCE-KEY-2026",
        "development",
        "REQUIRED_REPLACE_WITH_SECURE_HEX_32"
    ]

    @classmethod
    def validate(cls):
        """
        Executes a full suite of configuration checks.
        """
        logger.info("Starting ESOTERIC Enterprise Runtime Validation...")
        errors = []

        # 1. Presence Check
        for var in cls.REQUIRED_VARS:
            if not os.getenv(var):
                errors.append(f"MISSING_VAR: {var} is required but not set in environment.")

        # 2. Security Check: Secret Key
        secret_key = os.getenv("SECRET_KEY")
        if secret_key in cls.INSECURE_DEFAULTS:
            errors.append("INSECURE_SECRET: SECRET_KEY is set to an insecure default or placeholder.")
        
        if secret_key and len(secret_key) < 32:
            errors.append("WEAK_SECRET: SECRET_KEY should be at least 32 characters for HS256.")

        # 3. Environment Integrity
        env = os.getenv("ENVIRONMENT", "production")
        if env not in ["production", "staging", "development", "sandbox"]:
            errors.append(f"INVALID_ENV: {env} is not a recognized environment tier.")

        # 4. RBAC Policy Check
        rbac_file = os.getenv("RBAC_POLICY_FILE", "infra/config/rbac_policy.yaml")
        if not os.path.exists(rbac_file):
            logger.warning(f"RBAC_MISSING: Policy file not found at {rbac_file}. Using hardcoded fallbacks.")

        if errors:
            logger.error("Configuration Validation FAILED:")
            for error in errors:
                logger.error(f"  - {error}")
            
            if os.getenv("STRICT_CONFIG_VALIDATION", "False").lower() == "true":
                logger.critical("STRICT_MODE: Terminating due to configuration failures.")
                sys.exit(1)
            else:
                logger.warning("CONTINUING: Running in degraded/insecure state.")
        else:
            logger.info("ESOTERIC Runtime Validation: PASSED")

if __name__ == "__main__":
    ConfigValidator.validate()
