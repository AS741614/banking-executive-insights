import logging
from typing import List, Dict, Any, Tuple
from ai.onboarding.models.onboarding_models import DataOnboardingRequest, SchemaField

logger = logging.getLogger("esoteric_bank.onboarding.schema_validator")

class SchemaEvolutionValidator:
    """
    Institutional Schema Evolution Validator.
    Ensures that new data sources and schema changes are governance-compliant.
    """

    def validate_proposal(self, request: DataOnboardingRequest) -> Tuple[bool, List[str]]:
        """
        Validates the proposed schema against institutional standards.
        """
        reasons = []
        is_valid = True

        logger.info(f"Validating schema evolution for: {request.source_name}")

        for field in request.proposed_schema:
            # 1. PII Check
            if field.is_pii and not field.governance_tag:
                is_valid = False
                reasons.append(f"Field '{field.name}' is marked PII but lacks a governance tag.")

            # 2. Type Validation
            if field.data_type.upper() not in ["STRING", "INTEGER", "FLOAT", "BOOLEAN", "TIMESTAMP", "JSON"]:
                is_valid = False
                reasons.append(f"Unsupported data type '{field.data_type}' for field '{field.name}'.")

        # 3. Structural Consistency
        if not request.proposed_schema:
            is_valid = False
            reasons.append("Proposed schema cannot be empty.")

        return is_valid, reasons
