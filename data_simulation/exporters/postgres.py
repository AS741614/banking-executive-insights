import pandas as pd
from sqlalchemy import create_engine, text
import logging
from typing import List, Dict, Any

logger = logging.getLogger("data_simulation.exporters.postgres")

class PostgresExporter:
    """
    Exports the generated Python dataclasses into a PostgreSQL database.
    """
    def __init__(self, connection_string: str = "postgresql://dwh:dwh@localhost:5432/bank_dwh"):
        self.engine = create_engine(connection_string)
        self._ensure_schema_exists()
        
    def _ensure_schema_exists(self):
        try:
            with self.engine.begin() as conn:
                conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))
            logger.info("Verified schema 'raw' exists.")
        except Exception as e:
            logger.warning(f"Failed to verify/create schema 'raw': {e}")

    def export_customers(self, customers: List[Any]):
        logger.info(f"Exporting {len(customers)} customers to PostgreSQL...")
        df = pd.DataFrame([c.__dict__ for c in customers])
        df.to_sql("dim_customer_sim", self.engine, schema="raw", if_exists="replace", index=False)

    def export_accounts(self, accounts: List[Any]):
        logger.info(f"Exporting {len(accounts)} accounts to PostgreSQL...")
        df = pd.DataFrame([a.__dict__ for a in accounts])
        df.to_sql("dim_account_sim", self.engine, schema="raw", if_exists="replace", index=False)

    def export_transactions(self, transactions: List[Any]):
        logger.info(f"Exporting {len(transactions)} transactions to PostgreSQL...")
        df = pd.DataFrame([t.__dict__ for t in transactions])
        # Convert enum back to string
        df['txn_type'] = df['txn_type'].astype(str)
        df.to_sql("fact_transaction_sim", self.engine, schema="raw", if_exists="replace", index=False)

    def export_governance(self, events: List[Any]):
        if not events:
            return
        logger.info(f"Exporting {len(events)} governance events to PostgreSQL...")
        df = pd.DataFrame([e.__dict__ for e in events])
        df.to_sql("fact_governance_sim", self.engine, schema="raw", if_exists="replace", index=False)

    def export_treasury(self, signals: List[Any]):
        if not signals:
            return
        logger.info(f"Exporting {len(signals)} treasury signals to PostgreSQL...")
        df = pd.DataFrame([s.__dict__ for s in signals])
        df.to_sql("fact_treasury_sim", self.engine, schema="raw", if_exists="replace", index=False)
