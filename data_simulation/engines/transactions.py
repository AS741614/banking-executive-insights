import random
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from models.core import Account, Transaction, TransactionType, AccountType
import math

class TransactionEngine:
    """
    Simulates daily transaction volumes across the institutional network.
    Reacts to seasonal pressure and account tiering.
    """
    def __init__(self, accounts: List[Account], seed: int = 42):
        random.seed(seed)
        self.accounts = accounts
        self.account_map = {a.account_sk: a for a in accounts}
        self.active_accounts = [a for a in accounts if a.status == "ACTIVE"]

    def generate_daily_transactions(self, current_date: datetime.date, macro_state: dict) -> Tuple[List[Transaction], List[Account]]:
        """
        Generates transactions for a single day based on macro state (seasonality, etc.).
        Returns the generated transactions and the updated account balances.
        """
        daily_txns = []
        
        # Base volume: on average, 10% of accounts transact per day
        base_volume_fraction = 0.10
        
        # Adjust based on seasonality (month)
        month = current_date.month
        if month in [11, 12]:
            base_volume_fraction *= 1.4 # Holiday shopping spike
        elif month in [7, 8]:
            base_volume_fraction *= 0.8 # Summer lull
            
        # Determine number of transactions
        num_txns = int(len(self.active_accounts) * base_volume_fraction * random.uniform(0.9, 1.1))
        
        # Select transacting accounts
        transacting_accounts = random.choices(self.active_accounts, k=num_txns)
        
        for account in transacting_accounts:
            # Institutional accounts transact larger amounts
            if account.account_type == AccountType.TREASURY:
                txn_type = TransactionType.WIRE
                amount_mean = 500000
                amount_std = 100000
            elif account.account_type == AccountType.CREDIT:
                txn_type = TransactionType.CARD
                amount_mean = 500
                amount_std = 200
            else:
                txn_type = random.choices([TransactionType.ACH, TransactionType.CARD, TransactionType.INTERNAL_TRANSFER], weights=[0.4, 0.5, 0.1])[0]
                amount_mean = 1000 if account.account_type == AccountType.INVESTMENT else 150
                amount_std = 50
                
            amount = max(5.0, random.gauss(amount_mean, amount_std))
            
            # Determine flow direction (inflow vs outflow)
            # 60% chance of outflow (spending) for regular accounts
            is_outflow = random.random() < 0.60
            signed_amount = -amount if is_outflow else amount
            
            # Update account balance
            account.balance += signed_amount
            
            # Add some intra-day jitter to the timestamp
            txn_hour = random.randint(0, 23)
            txn_minute = random.randint(0, 59)
            txn_timestamp = datetime.combine(current_date, datetime.min.time()) + timedelta(hours=txn_hour, minutes=txn_minute)
            
            # Mock device/IP for card/web transactions
            device_id = f"DEV-{uuid.uuid4().hex[:12]}" if txn_type in [TransactionType.CARD, TransactionType.ACH] else None
            ip_address = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}" if device_id else None

            counterparty = None
            if txn_type == TransactionType.INTERNAL_TRANSFER:
                counterparty = random.choice(self.active_accounts).account_sk

            txn = Transaction(
                txn_id=f"TXN-{uuid.uuid4().hex[:16].upper()}",
                account_sk=account.account_sk,
                counterparty_account=counterparty,
                txn_type=txn_type,
                amount=round(amount, 2),
                signed_amount=round(signed_amount, 2),
                timestamp=txn_timestamp,
                device_id=device_id,
                ip_address=ip_address
            )
            daily_txns.append(txn)
            
        return daily_txns, self.active_accounts
