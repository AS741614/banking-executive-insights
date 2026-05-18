import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))
from pathlib import Path
import subprocess
import pandas as pd
from sqlalchemy import text

from src.db import get_engine

OUTPUT_DIR = ROOT / "ai/generated"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "executive_intelligence_summary.md"

engine = get_engine()

QUERY = """
SELECT
    region,
    segment,
    SUM(net_flow) AS net_flow,
    SUM(txn_count) AS txn_count
FROM mart.fact_account_month fam
JOIN mart.dim_account da
    ON fam.account_sk = da.account_sk
JOIN mart.dim_customer dc
    ON da.customer_sk = dc.customer_sk
JOIN mart.dim_branch db
    ON da.branch_sk = db.branch_sk
GROUP BY
    region,
    segment
ORDER BY
    net_flow DESC;
"""

print("======================================")
print("ESOTERIC Executive Intelligence Engine")
print("Generating cognitive banking briefing")
print("======================================")

df = pd.read_sql(text(QUERY), engine)

metrics = df.to_markdown(index=False)

PROMPT = f"""
You are the Chief Cognitive Intelligence Officer of ESOTERIC BANK.

You are responsible for:
- executive banking intelligence
- liquidity interpretation
- risk observability
- regional banking analysis
- customer segmentation intelligence
- operational anomaly interpretation
- governance-aware executive reporting
- strategic banking commentary
- AI-native financial observability

Analyze the following banking intelligence metrics and generate a professional executive intelligence briefing.

The report should resemble internal executive briefing material prepared for:
- banking executives
- treasury leadership
- risk management
- enterprise governance
- analytics leadership
- operational intelligence teams

Generate:

1. Executive Summary
2. Regional Liquidity Observations
3. Segment Performance Intelligence
4. Operational Risk Signals
5. Fraud / Anomaly Monitoring Considerations
6. Executive KPI Interpretation
7. Strategic Recommendations
8. Governance & Compliance Commentary
9. AI Augmentation Opportunities
10. Predictive Intelligence Recommendations

The tone must be:
- executive-grade
- strategic
- operationally intelligent
- technically authoritative
- governance-aware
- risk-conscious
- enterprise banking oriented

Do not explain methodology.
Do not output conversational commentary.
Output professional markdown only.

BANKING METRICS:
==================================================

{metrics}
"""

result = subprocess.run(
    ["gemini", "-p", PROMPT],
    capture_output=True,
    text=True
)

OUTPUT_FILE.write_text(result.stdout)

print("\nExecutive intelligence briefing generated:")
print(OUTPUT_FILE)
