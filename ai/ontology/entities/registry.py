import logging
from typing import Dict, List, Optional
from ai.ontology.entities.models import EntityDefinition, InstitutionalEntity, EntityCategory, SemanticProperty

logger = logging.getLogger("esoteric_bank.ontology.entity_registry")

class EntityOntologyRegistry:
    """
    Enterprise Entity Ontology Registry.
    Centralized repository for institutional concept definitions.
    """

    def __init__(self):
        self._registry: Dict[str, EntityDefinition] = {}
        self._initialize_core_ontology()

    def _initialize_core_ontology(self):
        """Bootstraps the registry with core banking entities."""
        core_entities = [
            EntityDefinition(
                entity=InstitutionalEntity(
                    entity_id="ENT-CUSTOMER",
                    name="Customer",
                    category=EntityCategory.ACTOR,
                    description="Institutional banking customer entity."
                ),
                properties=[
                    SemanticProperty(name="customer_id", data_type="string", is_required=True),
                    SemanticProperty(name="full_name", data_type="string", is_required=True),
                    SemanticProperty(name="compliance_tier", data_type="enum", governance_rule="KYC_TIERING")
                ]
            ),
            EntityDefinition(
                entity=InstitutionalEntity(
                    entity_id="ENT-TRANSACTION",
                    name="Transaction",
                    category=EntityCategory.ACTION,
                    description="Financial movement between accounts."
                ),
                properties=[
                    SemanticProperty(name="tx_id", data_type="string", is_required=True),
                    SemanticProperty(name="amount", data_type="float", is_required=True),
                    SemanticProperty(name="currency", data_type="string", is_required=True)
                ]
            )
        ]
        for definition in core_entities:
            self.register_entity(definition)

    def register_entity(self, definition: EntityDefinition):
        self._registry[definition.entity.entity_id] = definition
        logger.info(f"Registered institutional entity: {definition.entity.name} ({definition.entity.entity_id})")

    def get_entity(self, entity_id: str) -> Optional[EntityDefinition]:
        return self._registry.get(entity_id)

    def list_entities(self) -> List[EntityDefinition]:
        return list(self._registry.values())
