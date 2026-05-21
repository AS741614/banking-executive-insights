from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from datetime import datetime

class DomainIdentity(str, Enum):
    GOVERNANCE = "GOVERNANCE"
    ADAPTIVE = "ADAPTIVE"
    FRAUD = "FRAUD"
    OBSERVABILITY = "OBSERVABILITY"
    EXECUTIVE = "EXECUTIVE"
    REGULATORY = "REGULATORY"
    INFRASTRUCTURE = "INFRASTRUCTURE"

class ContractMaturity(str, Enum):
    DRAFT = "DRAFT"
    PROPOSED = "PROPOSED"
    STABLE = "STABLE"
    DEPRECATED = "DEPRECATED"

class ArchitectureContract(BaseModel):
    """
    Base Enterprise Architecture Contract for ESOTERIC BANK.
    Defines the boundaries and interface requirements for a domain.
    """
    model_config = ConfigDict(use_enum_values=True)
    
    contract_id: str
    domain: DomainIdentity
    version: str
    maturity: ContractMaturity = ContractMaturity.DRAFT
    owner: str
    
    # Bounded context definitions
    provided_capabilities: List[str]
    required_dependencies: List[str]
    
    # Interface specifications
    api_endpoints: List[str]
    published_events: List[str]
    consumed_events: List[str]
    
    # Governance metadata
    last_validated: Optional[datetime] = None
    compliance_grade: str = "PENDING"
    
class DomainRegistry(BaseModel):
    """
    Registry of all active architectural contracts across the enterprise.
    """
    active_contracts: Dict[DomainIdentity, ArchitectureContract] = {}
    
    def register_domain(self, contract: ArchitectureContract):
        self.active_contracts[contract.domain] = contract
