# Institutional Data Simulation Engine

## Overview
This bounded context contains the enterprise-grade synthetic data generation framework for ESOTERIC BANK. It simulates 24 months of highly realistic temporal banking evolution. 

It is designed strictly for testing observability, Tableau orchestration, governance escalation, and adaptive intelligence systems without requiring live production data.

## Core Simulation Domains
1. **Customer & Account Lifecycle**: Multi-tiered segments (Retail, Premier, Business, Institutional) with realistic balance distributions.
2. **Temporal & Macro Events**: 24-month progression with seasonality, holidays, and underlying liquidity pressure loops.
3. **Institutional Transactions**: Baseline ACH, Wire, Card, and Internal Transfers driven by time-of-day and cyclical volumes.
4. **Sophisticated Fraud & AML**:
   - Device Spoofing / Account Takeover (ATO) rings.
   - AML Structuring / Layering schemes targeting 10k CTR limits.
5. **Governance & Treasury Drift**:
   - Proxy Liquidity Coverage Ratio (LCR) deterioration.
   - Operational backlog alerts tied to transaction volume.
   - Policy escalations based on synthetic fraud multiples.

## Usage
To execute a local 24-month simulation:

```bash
PYTHONPATH=data_simulation python3 data_simulation/simulate.py
```

### PostgreSQL Integration
The `PostgresExporter` uses SQLAlchemy to automatically replace and seed the `raw` schema in the `bank_dwh` database:
- `raw.dim_customer_sim`
- `raw.dim_account_sim`
- `raw.fact_transaction_sim`
- `raw.fact_governance_sim`
- `raw.fact_treasury_sim`

## Constraints & Rules
- Do NOT generate pure random CSV spam.
- Preserve temporal continuity (fraud increases as liquidity degrades).
- Ensure all datasets are structurally compatible with `bank_dwh` ontology.
