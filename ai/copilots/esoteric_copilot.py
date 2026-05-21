import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT))

import subprocess
import pandas as pd
from sqlalchemy import text

from src.db import get_engine

engine = get_engine()

HEADER = """
====================================================================
ESOTERIC BANK
Cognitive Banking Intelligence Copilot
====================================================================

AI-Native Enterprise Banking Intelligence Layer

Capabilities:
- Executive Banking Intelligence
- Liquidity Interpretation
- Enterprise Risk Observability
- Fraud Intelligence Commentary
- Treasury Intelligence Support
- Governance-Aware Reporting
- Operational Banking Analysis
- AI-Augmented Strategic Insights
- Regional Concentration Interpretation
- Cognitive Banking Observability

====================================================================
"""

print(HEADER)

print("ESOTERIC Copilot Ready")
print("Type 'exit' to terminate cognitive session.\n")

while True:

    question = input("ESOTERIC COPILOT >>> ")

    if question.lower() == "exit":
        break

    QUERY = """
    WITH regional_summary AS (

        SELECT
            db.region,
            dc.segment,
            SUM(fam.net_flow) AS total_net_flow,
            SUM(fam.txn_count) AS total_txn_count,
            AVG(fam.net_flow) AS avg_net_flow

        FROM mart.fact_account_month fam

        JOIN mart.dim_account da
            ON fam.account_sk = da.account_sk

        JOIN mart.dim_customer dc
            ON da.customer_sk = dc.customer_sk

        JOIN mart.dim_branch db
            ON da.branch_sk = db.branch_sk

        GROUP BY
            db.region,
            dc.segment
    )

    SELECT
        *,
        CASE
            WHEN total_net_flow < 100000 THEN 'LIQUIDITY_PRESSURE'
            WHEN total_txn_count > 50000 THEN 'HIGH_ACTIVITY'
            ELSE 'NORMAL'
        END AS operational_signal

    FROM regional_summary

    ORDER BY
        total_net_flow DESC;
    """

    df = pd.read_sql(text(QUERY), engine)

    warehouse_context = df.to_markdown(index=False)

    PROMPT = f"""
You are the ESOTERIC BANK Cognitive Executive Intelligence Copilot.

You are operating as a regulated enterprise banking cognition layer embedded within the ESOTERIC AI-native banking intelligence platform.

Your role combines:
- executive banking strategy
- enterprise risk intelligence
- treasury observability
- fraud interpretation
- governance intelligence
- operational banking analytics
- AI-assisted executive reporting
- cognitive anomaly interpretation
- institutional financial observability

You must answer the executive user's banking intelligence query using the supplied enterprise warehouse intelligence context.

Your analysis must:

- identify operational banking patterns
- infer liquidity or concentration risks
- explain regional banking dynamics
- interpret customer segment behavior
- identify hidden governance concerns
- explain fraud or anomaly implications
- assess operational resilience
- provide strategic banking observations
- provide modernization recommendations where relevant
- emulate enterprise banking intelligence committee commentary

Your responses should resemble:
- executive banking briefings
- treasury intelligence commentary
- enterprise governance observations
- institutional risk analysis
- strategic banking intelligence memoranda

You are NOT a chatbot.

You are a cognitive banking intelligence system.

The tone must be:
- executive-grade
- analytically rigorous
- governance-aware
- risk-conscious
- technically authoritative
- operationally intelligent
- institutionally aligned

Critical Rules:
- Do not mention SQL
- Do not mention databases
- Do not mention AI limitations
- Do not explain methodology
- Do not simplify banking terminology
- Avoid generic summaries
- Provide enterprise-grade strategic commentary
- Focus on observability, governance, and operational intelligence

USER EXECUTIVE QUERY:
====================================================================

{question}

ENTERPRISE BANKING INTELLIGENCE CONTEXT:
====================================================================

{warehouse_context}
"""

    result = subprocess.run(
        ["gemini", "-p", PROMPT],
        capture_output=True,
        text=True
    )

    print("\n====================================================================")
    print("ESOTERIC EXECUTIVE INTELLIGENCE RESPONSE")
    print("====================================================================\n")

    print(result.stdout)

    print("\n====================================================================\n")
