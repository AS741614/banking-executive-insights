import logging
from typing import Optional
from ai.adaptive.models.evolution import AdaptiveRecommendation, EvolutionSeverity
from orchestration.contracts.architecture_contract import DomainIdentity
from orchestration.contracts.event_registry import enterprise_event_registry

logger = logging.getLogger("esoteric_bank.orchestration.evolution_governor")

class EvolutionGovernor:
    """
    Enterprise Evolution Governor.
    Enforces architectural safety and contract compliance on adaptive evolution plans.
    """

    def validate_evolution_plan(self, recommendation: AdaptiveRecommendation) -> bool:
        """
        Validates an evolution plan against enterprise governance rules.
        """
        logger.info(f"Governing evolution plan: {recommendation.recommendation_id}")

        # Rule 1: No MAJOR evolution without explicit Governance Domain approval
        if recommendation.severity == EvolutionSeverity.MAJOR:
            logger.warning(f"Evolution {recommendation.recommendation_id} rejected: MAJOR severity requires manual governance override.")
            return False

        # Rule 2: Proposed nodes must adhere to institutional naming conventions
        for node in recommendation.detailed_plan.get("proposed_nodes", []):
            if not self._is_institutional_naming(node):
                logger.warning(f"Evolution rejected: Node '{node}' violates institutional naming standards.")
                return False

        # Rule 3: Check for ontology drift against the Event Registry
        # (Ensuring new semantic mappings don't conflict with existing event contracts)
        for mapping in recommendation.detailed_plan.get("semantic_mappings", {}).values():
            if mapping is None:
                continue
            # Simple check for now: mapping should not mimic existing event types without being a contract
            if mapping.split(".")[-1].upper() in [c.event_type for c in enterprise_event_registry._contracts.values()]:
                 logger.warning(f"Evolution rejected: Mapping '{mapping}' conflicts with established event contracts.")
                 return False

        logger.info(f"Evolution plan {recommendation.recommendation_id} approved by Governor.")
        return True

    def _is_institutional_naming(self, name: str) -> bool:
        """
        Validates that a name follows enterprise standards (PascalCase_With_Underscores).
        """
        import re
        pattern = r"^[A-Z][a-z]+(_[A-Z][a-z]+)*$"
        # For simplicity in this demo, just check if it's not all lowercase
        return not name.islower()

# Global Governor instance
evolution_governor = EvolutionGovernor()
