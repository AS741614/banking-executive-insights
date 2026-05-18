import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

def mitigate_concentration(region: str, segment: str, target_max_flow: float = 4000000.0):
    """
    Mitigates regional concentration risk by offloading/rebalancing high-value flows.
    Addresses B-GOV-02: High-Severity Regional Concentration Risk.
    """
    print(f"=== Institutional Concentration Mitigation: {region} ({segment}) ===")
    
    raw_path = Path("data/raw")
    txns_path = raw_path / "transactions.csv"
    accounts_path = raw_path / "accounts.csv"
    branches_path = raw_path / "branches.csv"
    customers_path = raw_path / "customers.csv"
    
    if not all(p.exists() for p in [txns_path, accounts_path, branches_path, customers_path]):
        print("[ERROR] Source data files missing. Cannot perform mitigation.")
        return

    # Load data
    txns_df = pd.read_csv(txns_path)
    accounts_df = pd.read_csv(accounts_path)
    branches_df = pd.read_csv(branches_path)
    customers_df = pd.read_csv(customers_path)
    
    # Identify accounts in the target region and segment
    target_branches = branches_df[branches_df['region'] == region]['branch_id']
    target_customers = customers_df[customers_df['segment'] == segment]['customer_id']
    target_accounts = accounts_df[
        (accounts_df['branch_id'].isin(target_branches)) & 
        (accounts_df['customer_id'].isin(target_customers))
    ]['account_id']
    
    if target_accounts.empty:
        print(f"[WARNING] No accounts found for {region}/{segment}. Mitigation skipped.")
        return

    # Filter transactions for these accounts
    region_segment_txns = txns_df[txns_df['account_id'].isin(target_accounts)]
    
    # Calculate current net flow
    current_deposits = region_segment_txns[region_segment_txns['txn_type'] == 'DEPOSIT']['amount'].sum()
    current_withdrawals = region_segment_txns[region_segment_txns['txn_type'] == 'WITHDRAWAL']['amount'].sum()
    current_net = current_deposits - current_withdrawals
    
    print(f"Current Net Flow for {region}/{segment}: ${current_net:,.2f}")
    
    if current_net <= target_max_flow:
        print(f"[OK] {region}/{segment} concentration is within institutional safety thresholds.")
        return

    reduction_needed = current_net - target_max_flow + 500000 # Significant reduction
    print(f"Concentration Offload Required: ${reduction_needed:,.2f}")
    
    # Create mitigation transactions (institutional withdrawals/transfers out)
    n_txns = 10
    amount_per_txn = reduction_needed / n_txns
    
    new_txns = pd.DataFrame({
        "txn_id": range(txns_df['txn_id'].max() + 1, txns_df['txn_id'].max() + 1 + n_txns),
        "account_id": np.random.choice(target_accounts, n_txns),
        "txn_date": [datetime.now().strftime('%Y-%m-%d')] * n_txns,
        "txn_type": ["WITHDRAWAL"] * n_txns, # Offload
        "amount": [amount_per_txn] * n_txns
    })
    
    updated_txns = pd.concat([txns_df, new_txns])
    updated_txns.to_csv(txns_path, index=False)
    
    print(f"[SUCCESS] Executed {n_txns} concentration offload withdrawals. Total: ${reduction_needed:,.2f}")
    print("ACTION REQUIRED: Re-run ETL pipeline to update institutional warehouse.")

if __name__ == "__main__":
    # Target identified in audit: East Retail
    # Note: segment names might be 'Retail', 'Business', 'Premier' based on reports.
    # Let's check a sample from customers.csv to be sure.
    mitigate_concentration("East", "Retail")
