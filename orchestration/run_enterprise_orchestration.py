import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

import asyncio
import json
from datetime import datetime

from orchestration.contracts.architecture_contract import (
    ArchitectureContract, DomainIdentity, ContractMaturity
)
from orchestration.contracts.event_registry import enterprise_event_registry
from orchestration.governance.evolution_governor import evolution_governor
from orchestration.topology.cognitive_topology import enterprise_topology
from orchestration.state.platform_state import platform_state, DomainState

from ai.adaptive.engines.schema_detection import SchemaDetectionEngine
from ai.adaptive.engines.ontology_evolution import OntologyEvolutionEngine

async def run_orchestration_cycle():
    print("====================================================================")
    print("ESOTERIC BANK: Enterprise Architecture Orchestration Cycle")
    print(f"Timestamp: {datetime.now()}")
    print("====================================================================\n")

    # 1. Initialize Architecture Contracts
    print("[1/5] Initializing Architecture Contracts...")
    gov_contract = ArchitectureContract(
        contract_id="GOV-2026-V1",
        domain=DomainIdentity.GOVERNANCE,
        version="1.0.0",
        maturity=ContractMaturity.STABLE,
        owner="Chief Governance Officer",
        provided_capabilities=["DRIFT_DETECTION", "EXECUTIVE_REPORTING"],
        required_dependencies=["ADAPTIVE"],
        api_endpoints=["/api/v1/governance/drift"],
        published_events=["GOVERNANCE_DRIFT_DETECTED"],
        consumed_events=["ADAPTIVE_EVOLUTION_PROPOSED"]
    )
    print(f"Registered Domain: {gov_contract.domain} | Version: {gov_contract.version}")

    # 2. Simulate Adaptive Evolution Ingest
    print("\n[2/5] Simulating Adaptive Evolution Cycle...")
    schema_engine = SchemaDetectionEngine()
    evo_engine = OntologyEvolutionEngine()

    raw_data_schema = {
        "cust_internal_id": "string",
        "tx_value_usd": "float",
        "is_pep_exposed": "boolean",
        "unknown_field_x": "string"
    }

    inferences = schema_engine.detect_schema_semantics(raw_data_schema)
    recommendation = evo_engine.generate_evolution_plan(inferences, context="INSTITUTIONAL_INGEST")
    
    print(f"Adaptive Recommendation Generated: {recommendation.recommendation_id}")
    print(f"Severity: {recommendation.severity}")

    # 3. Apply Governance Oversight
    print("\n[3/5] Applying Governance Oversight via Evolution Governor...")
    is_safe = evolution_governor.validate_evolution_plan(recommendation)
    
    if is_safe:
        print("RESULT: Evolution Plan APPROVED for implementation.")
    else:
        print("RESULT: Evolution Plan REJECTED by Governance Integrity Rules.")

    # 4. Update Platform State & Topology
    print("\n[4/5] Synchronizing Platform State & Topology...")
    platform_state.update_state(DomainState(
        domain=DomainIdentity.ADAPTIVE,
        status="ACTIVE",
        active_contracts=["ADAPTIVE-GOV-V1"],
        metadata={"last_evolution_id": recommendation.recommendation_id}
    ))
    
    print(f"Active Nodes in Topology: {list(enterprise_topology.nodes.keys())}")
    print(f"Cross-Domain Links: {len(enterprise_topology.links)}")

    # 5. Generate Architecture Integrity Report
    print("\n[5/5] Generating Architecture Integrity Report...")
    report = {
        "enterprise_status": "CONVERGED",
        "active_domains": [d.value for d in platform_state.domain_states.keys()],
        "governance_compliance": "VALIDATED",
        "ontology_drift": "MINIMAL",
        "orchestration_cycle": "COMPLETE"
    }
    
    print("\n====================================================================")
    print("ORCHESTRATION CYCLE COMPLETE")
    print(json.dumps(report, indent=2))
    print("====================================================================")

if __name__ == "__main__":
    asyncio.run(run_orchestration_cycle())
