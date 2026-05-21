import logging
from typing import List, Dict, Set
from worldmodel.models.world_models import OperationalRelationship, OperationalRelationshipType

logger = logging.getLogger("esoteric_bank.worldmodel.relationship_graph")

class OperationalRelationshipGraph:
    """
    Enterprise Operational Relationship Graph.
    Models the complex interdependencies and governance flows of the institution.
    """

    def __init__(self):
        self._relationships: List[OperationalRelationship] = []
        self._adj_list: Dict[str, Set[str]] = {}

    def add_relationship(self, rel: OperationalRelationship):
        self._relationships.append(rel)
        if rel.source_id not in self._adj_list:
            self._adj_list[rel.source_id] = set()
        self._adj_list[rel.source_id].add(rel.target_id)
        logger.info(f"Established relationship: {rel.source_id} {rel.relationship_type} {rel.target_id}")

    def get_dependencies(self, entity_id: str) -> List[str]:
        """Returns a list of entities that the given entity depends on."""
        return [r.target_id for r in self._relationships 
                if r.source_id == entity_id and r.relationship_type == OperationalRelationshipType.DEPENDS_ON]

    def get_governing_bodies(self, entity_id: str) -> List[str]:
        """Returns a list of entities that govern the given entity."""
        return [r.source_id for r in self._relationships 
                if r.target_id == entity_id and r.relationship_type == OperationalRelationshipType.GOVERNS]

    def check_impact_path(self, start_id: str, target_id: str, visited: Set[str] = None) -> bool:
        """Determines if there is a dependency or governance path between two entities."""
        if visited is None: visited = set()
        if start_id == target_id: return True
        
        visited.add(start_id)
        for neighbor in self._adj_list.get(start_id, set()):
            if neighbor not in visited:
                if self.check_impact_path(neighbor, target_id, visited):
                    return True
        return False
