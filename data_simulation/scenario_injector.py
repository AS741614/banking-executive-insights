import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta

class ScenarioInjector:
    """
    Utilities for injecting stress data into the raw CSV datasets.
    """
    
    def __init__(self, raw_path: str = "data/raw"):
        self.raw_path = Path(raw_path)

    def inject_liquidity_drain(self, region: str, amount_per_txn: float = 1000000.0, n_txns: int = 50):
        """
        Simulates a massive capital outflow in a specific region.
        """
        # Load transactions
        txns_df = pd.read_csv(self.raw_path / "transactions.csv")
        accounts_df = pd.read_csv(self.raw_path / "accounts.csv")
        branches_df = pd.read_csv(self.raw_path / "branches.csv")
        
        # Find accounts in the target region
        target_branches = branches_df[branches_df['region'] == region]['branch_id']
        target_accounts = accounts_df[accounts_df['branch_id'].isin(target_branches)]['account_id']
        
        if target_accounts.empty:
            raise ValueError(f"No accounts found for region: {region}")
            
        # Create drain transactions
        new_txns = pd.DataFrame({
            "txn_id": range(txns_df['txn_id'].max() + 1, txns_df['txn_id'].max() + 1 + n_txns),
            "account_id": np.random.choice(target_accounts, n_txns),
            "txn_date": [datetime.now().strftime('%Y-%m-%d')] * n_txns,
            "txn_type": ["WITHDRAWAL"] * n_txns,
            "amount": [amount_per_txn] * n_txns
        })
        
        # Append and save
        updated_txns = pd.concat([txns_df, new_txns])
        updated_txns.to_csv(self.raw_path / "transactions.csv", index=False)
        return len(new_txns)

    def inject_fraud_burst(self, account_id: int, n_txns: int = 20):
        """
        Simulates an account takeover (burst of high-velocity withdrawals).
        """
        txns_df = pd.read_csv(self.raw_path / "transactions.csv")
        
        new_txns = pd.DataFrame({
            "txn_id": range(txns_df['txn_id'].max() + 1, txns_df['txn_id'].max() + 1 + n_txns),
            "account_id": [account_id] * n_txns,
            "txn_date": [datetime.now().strftime('%Y-%m-%d')] * n_txns,
            "txn_type": ["WITHDRAWAL"] * n_txns,
            "amount": [np.random.uniform(5000, 15000) for _ in range(n_txns)]
        })
        
        updated_txns = pd.concat([txns_df, new_txns])
        updated_txns.to_csv(self.raw_path / "transactions.csv", index=False)
        return len(new_txns)
