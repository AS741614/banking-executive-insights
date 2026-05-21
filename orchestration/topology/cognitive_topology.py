from typing import List, Dict, Any
from pydantic import BaseModel
from orchestration.contracts.architecture_contract import DomainIdentity

class CognitionNode(BaseModel):
    node_id: str
    domain: DomainIdentity
    capabilities: List[str]
    is_active: bool = True

class CognitionLink(BaseModel):
    source_node: str
    target_node: str
    flow_type: str # e.g., EVENT, API, KNOWLEDGE
    contract_id: str

class CognitiveTopology(BaseModel):
    """
    Maps the enterprise cognitive architecture.
    Provides visibility into cross-domain knowledge flows.
    """
    nodes: Dict[str, CognitionNode] = {}
    links: List[CognitionLink] = []

    def register_node(self, node: CognitionNode):
        self._nodes[node.node_id] = node

    def add_link(self, link: CognitionLink):
        self.links.append(link)

# Global Topology instance
enterprise_topology = CognitiveTopology()

# Initialize core topology
enterprise_topology.nodes["GOVERNANCE_ENGINE"] = CognitionNode(
    node_id="GOVERNANCE_ENGINE",
    domain=DomainIdentity.GOVERNANCE,
    capabilities=["DRIFT_DETECTION", "EXECUTIVE_REPORTING"]
)

enterprise_topology.nodes["ADAPTIVE_ENGINE"] = CognitionNode(
    node_id="ADAPTIVE_ENGINE",
    domain=DomainIdentity.ADAPTIVE,
    capabilities=["ONTOLOGY_EVOLUTION", "SCHEMA_INFERENCE"]
)

enterprise_topology.add_link(
    CognitionLink(
        source_node="ADAPTIVE_ENGINE",
        target_node="GOVERNANCE_ENGINE",
        flow_type="KNOWLEDGE",
        contract_id="ADAPTIVE_GOVERNANCE_V1"
    )
)
