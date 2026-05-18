import logging
from typing import Dict, List, Optional
from worldmodel.models.world_models import InstitutionalEntity, InstitutionalEntityType

logger = logging.getLogger("esoteric_bank.worldmodel.entity_registry")

class InstitutionalEntityRegistry:
    """
    Enterprise Institutional Entity Registry.
    Maintains the authoritative catalog of organizational units and processes.
    """

    def __init__(self):
        self._entities: Dict[str, InstitutionalEntity] = {}
        self._initialize_core_topology()

    def _initialize_core_topology(self):
        """Bootstraps the registry with foundational organizational units."""
        core_units = [
            InstitutionalEntity(
                entity_id="ORG-BOARD",
                name="Board of Directors",
                entity_type=InstitutionalEntityType.ORGANIZATION_UNIT,
                description="Supreme governing body of the institution.",
                governance_clearance="TIER_4"
            ),
            InstitutionalEntity(
                entity_id="ORG-TREASURY",
                name="Global Treasury",
                entity_type=InstitutionalEntityType.ORGANIZATION_UNIT,
                description="Unit responsible for liquidity and capital management.",
                governance_clearance="TIER_3"
            ),
            InstitutionalEntity(
                entity_id="ORG-COMPLIANCE",
                name="Enterprise Compliance",
                entity_type=InstitutionalEntityType.ORGANIZATION_UNIT,
                description="Unit responsible for regulatory adherence and AML.",
                governance_clearance="TIER_3"
            )
        ]
        for unit in core_units:
            self.register_entity(unit)

    def register_entity(self, entity: InstitutionalEntity):
        self._entities[entity.entity_id] = entity
        logger.info(f"Registered institutional entity: {entity.name} [{entity.entity_id}]")

    def get_entity(self, entity_id: str) -> Optional[InstitutionalEntity]:
        return self._entities.get(entity_id)

    def list_entities_by_type(self, entity_type: InstitutionalEntityType) -> List[InstitutionalEntity]:
        return [e for e in self._entities.values() if e.entity_type == entity_type]
