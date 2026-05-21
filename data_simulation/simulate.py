import logging
import os
from datetime import date
from engines.temporal import TemporalEngine
from engines.customer import CustomerEngine
from engines.transactions import TransactionEngine
from engines.fraud_aml import FraudAMLEngine
from engines.treasury_governance import GovernanceTreasuryEngine
from exporters.postgres import PostgresExporter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("data_simulation.orchestrator")

def run_simulation(start_year: int = 2024, start_month: int = 1, months_to_simulate: int = 24, num_customers: int = 1000):
    start_date = date(start_year, start_month, 1)
    
    # Approx calculation for end date
    end_month = start_month + months_to_simulate
    end_year = start_year + (end_month - 1) // 12
    end_month = ((end_month - 1) % 12) + 1
    end_date = date(end_year, end_month, 1)
    
    logger.info(f"Starting ESOTERIC BANK Institutional Simulation from {start_date} to {end_date}")
    
    # 1. Initialize Engines
    temporal = TemporalEngine(start_date, end_date)
    customer_engine = CustomerEngine()
    fraud_engine = FraudAMLEngine()
    gov_engine = GovernanceTreasuryEngine()
    exporter = PostgresExporter()
    
    # 2. Generate Initial Population
    logger.info("Generating initial customer base and accounts...")
    customers, accounts = customer_engine.generate_population(start_date, count=num_customers)
    
    txn_engine = TransactionEngine(accounts)
    
    all_transactions = []
    all_gov_events = []
    all_treasury_signals = []
    
    # 3. Time Loop
    logger.info("Starting temporal simulation loop...")
    while not temporal.is_finished:
        current_date = temporal.current_date
        macro_state = temporal.get_current_state()
        
        # A. Normal Transactions
        daily_txns, active_accounts = txn_engine.generate_daily_transactions(current_date, macro_state)
        
        # B. Fraud & AML Injections
        daily_txns = fraud_engine.inject_anomalies(daily_txns, active_accounts, current_date, macro_state)
        
        # C. Governance & Treasury Signals
        gov_events, treasury_signals = gov_engine.generate_daily_signals(current_date, macro_state)
        
        all_transactions.extend(daily_txns)
        all_gov_events.extend(gov_events)
        all_treasury_signals.extend(treasury_signals)
        
        if current_date.day == 1:
            logger.info(f"Simulated Month: {current_date.strftime('%Y-%m')} | txns={len(daily_txns)} | LCR Proxy={macro_state['liquidity_pressure']:.2f}")
            
        temporal.advance_day()

    logger.info(f"Simulation Complete. Total Transactions: {len(all_transactions)}")
    
    # 4. Export
    # Optional: If DB isn't running, we can skip or catch error
    try:
        exporter.export_customers(customers)
        exporter.export_accounts(accounts)
        exporter.export_transactions(all_transactions)
        exporter.export_governance(all_gov_events)
        exporter.export_treasury(all_treasury_signals)
        logger.info("Successfully exported synthetic intelligence to PostgreSQL.")
    except Exception as e:
        logger.warning(f"Could not export to PostgreSQL (is it running?): {e}")

if __name__ == "__main__":
    # For testing, we run a smaller volume
    run_simulation(num_customers=500)
