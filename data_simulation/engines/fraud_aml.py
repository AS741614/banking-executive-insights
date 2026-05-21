import random
import uuid
from datetime import datetime, timedelta
from typing import List, Tuple
from models.core import Account, Transaction, TransactionType

class FraudAMLEngine:
    """
    Injects sophisticated fraud rings and AML layering patterns into the transaction stream.
    """
    def __init__(self, seed: int = 42):
        random.seed(seed)
        # Store active fraud rings (shared devices/IPs across accounts)
        self.active_rings = [] 

    def inject_anomalies(self, daily_txns: List[Transaction], all_accounts: List[Account], current_date: datetime.date, macro_state: dict) -> List[Transaction]:
        """
        Takes the baseline daily transactions and injects coordinated fraud and AML behavior.
        The injection rate scales with the 'fraud_multiplier' macro state.
        """
        fraud_multiplier = macro_state.get("fraud_multiplier", 1.0)
        
        # 1. Device Spoofing / Account Takeover Ring
        # Multiple accounts suddenly using the same device ID to drain funds
        ring_prob = 0.05 * fraud_multiplier
        if random.random() < ring_prob:
            daily_txns.extend(self._simulate_ato_ring(all_accounts, current_date))
            
        # 2. AML Layering (Smurfing)
        # Structuring large deposits into smaller transactions just below reporting thresholds
        layering_prob = 0.02 * fraud_multiplier
        if random.random() < layering_prob:
            daily_txns.extend(self._simulate_aml_layering(all_accounts, current_date))
            
        return daily_txns

    def _simulate_ato_ring(self, accounts: List[Account], current_date: datetime.date) -> List[Transaction]:
        """Simulates an Account Takeover ring sharing a device."""
        compromised_accounts = random.sample(accounts, k=random.randint(3, 8))
        malicious_device = f"DEV-FRAUD-{uuid.uuid4().hex[:8]}"
        malicious_ip = f"185.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
        
        fraud_txns = []
        base_time = datetime.combine(current_date, datetime.min.time()) + timedelta(hours=random.randint(1, 4)) # Usually late night/early morning
        
        for idx, account in enumerate(compromised_accounts):
            # Attempt to drain max available balance
            drain_amount = account.balance * random.uniform(0.8, 1.0)
            if drain_amount < 50:
                continue
                
            txn_time = base_time + timedelta(minutes=idx * random.randint(2, 10))
            
            txn = Transaction(
                txn_id=f"TXN-FRAUD-{uuid.uuid4().hex[:12].upper()}",
                account_sk=account.account_sk,
                counterparty_account="EXTERNAL_WALLET",
                txn_type=TransactionType.WIRE, # Fast money movement
                amount=round(drain_amount, 2),
                signed_amount=-round(drain_amount, 2),
                timestamp=txn_time,
                device_id=malicious_device,
                ip_address=malicious_ip,
                is_flagged_fraud=False # Becomes True if detection engine catches it
            )
            account.balance += txn.signed_amount # Execute the drain
            fraud_txns.append(txn)
            
        return fraud_txns

    def _simulate_aml_layering(self, accounts: List[Account], current_date: datetime.date) -> List[Transaction]:
        """Simulates structuring deposits to avoid 10k CTR (Currency Transaction Report)."""
        mule_accounts = random.sample(accounts, k=random.randint(4, 10))
        target_account = random.choice(accounts)
        
        aml_txns = []
        base_time = datetime.combine(current_date, datetime.min.time()) + timedelta(hours=9)
        
        for idx, mule in enumerate(mule_accounts):
            # Amount just below 10k threshold
            amount = random.uniform(8500, 9900)
            txn_time = base_time + timedelta(hours=idx * random.uniform(0.5, 2.0))
            
            # 1. Mule receives cash (simulated as ACH inflow)
            inflow = Transaction(
                txn_id=f"TXN-AML-IN-{uuid.uuid4().hex[:10].upper()}",
                account_sk=mule.account_sk,
                counterparty_account=None,
                txn_type=TransactionType.ACH,
                amount=round(amount, 2),
                signed_amount=round(amount, 2),
                timestamp=txn_time - timedelta(minutes=30),
                device_id=None,
                ip_address=None,
                is_flagged_aml=False
            )
            mule.balance += inflow.signed_amount
            aml_txns.append(inflow)
            
            # 2. Mule wires to target account (layering)
            outflow = Transaction(
                txn_id=f"TXN-AML-OUT-{uuid.uuid4().hex[:10].upper()}",
                account_sk=mule.account_sk,
                counterparty_account=target_account.account_sk,
                txn_type=TransactionType.INTERNAL_TRANSFER,
                amount=round(amount, 2),
                signed_amount=-round(amount, 2),
                timestamp=txn_time,
                device_id=f"DEV-{uuid.uuid4().hex[:8]}",
                ip_address=None,
                is_flagged_aml=False
            )
            mule.balance += outflow.signed_amount
            target_account.balance += amount
            aml_txns.append(outflow)
            
        return aml_txns
