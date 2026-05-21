from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Optional, Dict, Any
from enum import Enum

class CustomerSegment(str, Enum):
    RETAIL = "Retail"
    PREMIER = "Premier"
    BUSINESS = "Business"
    INSTITUTIONAL = "Institutional"

class AccountType(str, Enum):
    CHECKING = "Checking"
    SAVINGS = "Savings"
    TREASURY = "Treasury"
    CREDIT = "Credit"
    INVESTMENT = "Investment"

class TransactionType(str, Enum):
    WIRE = "Wire"
    ACH = "ACH"
    CARD = "Card"
    INTERNAL_TRANSFER = "Internal_Transfer"
    FEE = "Fee"

@dataclass
class Customer:
    customer_sk: str
    first_name: str
    last_name: str
    segment: CustomerSegment
    country: str
    region: str
    kyc_status: str
    onboarding_date: date
    risk_score: float

@dataclass
class Account:
    account_sk: str
    customer_sk: str
    branch_sk: str
    product_sk: str
    account_type: AccountType
    open_date: date
    balance: float
    status: str
    currency: str = "USD"

@dataclass
class Transaction:
    txn_id: str
    account_sk: str
    counterparty_account: Optional[str]
    txn_type: TransactionType
    amount: float
    signed_amount: float
    timestamp: datetime
    device_id: Optional[str]
    ip_address: Optional[str]
    is_flagged_fraud: bool = False
    is_flagged_aml: bool = False

@dataclass
class GovernanceEvent:
    event_id: str
    event_type: str
    severity: str # LOW, MEDIUM, HIGH, CRITICAL
    entity_id: str
    entity_type: str # CUSTOMER, ACCOUNT, REGION, BRANCH
    description: str
    timestamp: datetime
    resolution_status: str = "OPEN"

@dataclass
class TreasurySignal:
    signal_id: str
    metric_name: str
    value: float
    timestamp: datetime
    drift_status: str
    region: Optional[str] = None
