import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

import subprocess
import pandas as pd
from sqlalchemy import text

from src.db import get_engine

OUTPUT_DIR = ROOT / "ai/generated"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "risk_intelligence_report.md"

engine = get_engine()

QUERY = """
WITH customer_activity AS (
    SELECT
        dc.customer_id,
        dc.segment,
        db.region,
        COUNT(ft.txn_id) AS txn_count,
        SUM(ft.signed_amount) AS net_flow,
        AVG(ABS(ft.amount)) AS avg_txn_size,
        MAX(ABS(ft.amount)) AS max_txn_size
    FROM mart.fact_transaction ft
    JOIN mart.dim_account da
        ON ft.account_sk = da.account_sk
    JOIN mart.dim_customer dc
        ON da.customer_sk = dc.customer_sk
    JOIN mart.dim_branch db
        ON da.branch_sk = db.branch_sk
    GROUP BY
        dc.customer_id,
        dc.segment,
        db.region
)

SELECT
    *,
    CASE
        WHEN txn_count > 120 THEN 'HIGH_VELOCITY'
        WHEN net_flow < -5000 THEN 'NEGATIVE_LIQUIDITY'
        WHEN max_txn_size > 5000 THEN 'LARGE_TRANSACTION'
        ELSE 'NORMAL'
    END AS risk_signal
FROM customer_activity
ORDER BY
    txn_count DESC,
    net_flow ASC;
"""

print("===================================================")
print("ESOTERIC Cognitive Risk Intelligence Engine Online")
print("Generating enterprise risk observability report...")
print("===================================================")

df = pd.read_sql(text(QUERY), engine)

risk_summary = df.to_markdown(index=False)

PROMPT = f"""
You are the Chief Risk Intelligence Officer of ESOTERIC BANK.

You are operating inside an AI-native enterprise banking observability and cognitive intelligence platform.

Your responsibilities include:
- enterprise banking risk intelligence
- fraud observability
- AML anomaly interpretation
- liquidity deterioration monitoring
- transaction surveillance
- regional concentration analysis
- operational risk interpretation
- governance-aware intelligence reporting
- cognitive anomaly explanation
- executive risk escalation support

Analyze the following enterprise banking risk intelligence dataset.

Generate a highly advanced enterprise-grade risk intelligence briefing suitable for:
- CRO office
- enterprise risk committees
- AML governance teams
- fraud operations
- treasury leadership
- executive governance boards
- operational intelligence leadership

The report must contain:

1. Executive Risk Summary
2. Transaction Velocity Intelligence
3. Liquidity Deterioration Signals
4. Regional Concentration Risk Analysis
5. AML & Fraud Observability Commentary
6. Suspicious Activity Intelligence
7. Operational Banking Risk Signals
8. Governance & Regulatory Exposure
9. Predictive Risk Intelligence Recommendations
10. AI Augmentation Opportunities
11. Banking Observability Findings
12. Enterprise Risk Mitigation Recommendations
13. Cognitive Risk Escalation Priorities
14. Strategic Banking Stability Assessment

The analysis should:
- identify suspicious patterns
- explain concentration risks
- interpret abnormal liquidity behavior
- evaluate operational instability indicators
- identify hidden governance concerns
- infer systemic banking weaknesses
- suggest modernization opportunities
- emulate enterprise-grade risk committee reporting

The tone must be:
- executive-grade
- governance-oriented
- risk-conscious
- technically authoritative
- strategically analytical
- audit-aware
- enterprise banking aligned

Do not explain methodology.
Do not output conversational commentary.
Do not simplify technical banking terminology.
Output professional markdown only.

BANKING RISK DATASET:
==================================================

{risk_summary}
"""

result = subprocess.run(
    ["gemini", "-p", PROMPT],
    capture_output=True,
    text=True
)

OUTPUT_FILE.write_text(result.stdout)

print("\nEnterprise risk intelligence report generated:")
print(OUTPUT_FILE)
