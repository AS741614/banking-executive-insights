import numpy as np
import pandas as pd
from pathlib import Path
from faker import Faker

fake = Faker()
Faker.seed(42)
np.random.seed(42)

RAW = Path("data/raw")
RAW.mkdir(parents=True, exist_ok=True)

N_CUST = 5000
N_ACCT = 8000
N_TXN = 200000

regions = ["North", "South", "East", "West"]

branches = pd.DataFrame({
    "branch_id": range(1, 21),
    "branch_name": [f"Branch {i:02d}" for i in range(1, 21)],
    "city": [fake.city() for _ in range(20)],
    "region": np.random.choice(regions, 20),
})

products = pd.DataFrame({
    "product_id": [1, 2, 3, 4, 5],
    "product_name": [
        "Current Account",
        "Savings",
        "Mortgage",
        "Personal Loan",
        "Credit Card"
    ],
    "product_type": [
        "Deposit",
        "Deposit",
        "Lending",
        "Lending",
        "Lending"
    ],
})

segments = np.random.choice(
    ["Retail", "Premier", "Business"],
    N_CUST,
    p=[0.7, 0.2, 0.1]
)

customers = pd.DataFrame({
    "customer_id": range(1, N_CUST + 1),
    "full_name": [fake.name() for _ in range(N_CUST)],
    "segment": segments,
    "country": np.random.choice(
        ["IE", "GB", "US", "DE"],
        N_CUST
    ),
    "onboarded_date": pd.to_datetime(
        np.random.choice(
            pd.date_range("2018-01-01", "2024-12-31"),
            N_CUST
        )
    ),
})

accounts = pd.DataFrame({
    "account_id": range(1, N_ACCT + 1),
    "customer_id": np.random.randint(
        1,
        N_CUST + 1,
        N_ACCT
    ),
    "product_id": np.random.randint(1, 6, N_ACCT),
    "branch_id": np.random.randint(1, 21, N_ACCT),
    "open_date": pd.to_datetime(
        np.random.choice(
            pd.date_range("2019-01-01", "2025-06-30"),
            N_ACCT
        )
    ),
    "status": np.random.choice(
        ["ACTIVE", "DORMANT", "CLOSED"],
        N_ACCT,
        p=[0.85, 0.10, 0.05]
    ),
})

txn_types = [
    "DEPOSIT",
    "WITHDRAWAL",
    "FEE",
    "INTEREST",
    "TRANSFER"
]

transactions = pd.DataFrame({
    "txn_id": range(1, N_TXN + 1),
    "account_id": np.random.randint(
        1,
        N_ACCT + 1,
        N_TXN
    ),
    "txn_date": pd.to_datetime(
        np.random.choice(
            pd.date_range("2023-01-01", "2025-06-30"),
            N_TXN
        )
    ),
    "txn_type": np.random.choice(
        txn_types,
        N_TXN
    ),
    "amount": np.round(
        np.random.gamma(2.0, 250.0, N_TXN),
        2
    ),
})

datasets = [
    ("branches", branches),
    ("products", products),
    ("customers", customers),
    ("accounts", accounts),
    ("transactions", transactions),
]

for name, df in datasets:
    df.to_csv(RAW / f"{name}.csv", index=False)
    print(f"Wrote {name}: {len(df):,} rows")
