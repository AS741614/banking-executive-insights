import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT))

from datetime import datetime
import subprocess
import json
import pandas as pd
from sqlalchemy import text

from src.db import get_engine

engine = get_engine()

REPORT_DIR = ROOT / "ai/governance/reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

REPORT_FILE = REPORT_DIR / f"governance_cognition_report_{timestamp}.md"

HEADER = f"""
====================================================================
ESOTERIC BANK
Autonomous Governance Cognition Engine
====================================================================

AI-Native Governance Observability Architecture

Capabilities:
- Institutional Governance Monitoring
- Banking Integrity Validation
- Treasury Governance Observability
- Governance Drift Detection
- Operational Reliability Intelligence
- Enterprise Oversight Cognition
- Banking Stability Governance Analysis
- AI-Augmented Governance Intelligence
- Executive Oversight Monitoring

Governance Intelligence Timestamp:
{timestamp}

====================================================================
"""

print(HEADER)

QUERY = """
WITH governance_observability AS (

    SELECT
        db.region,
        dc.segment,

        COUNT(*) AS account_volume,

        SUM(fam.net_flow) AS total_net_flow,

        AVG(fam.net_flow) AS avg_net_flow,

        SUM(fam.txn_count) AS total_txn_count

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

SELECT *
FROM governance_observability;
"""

df = pd.read_sql(text(QUERY), engine)

governance_events = []

def register_governance_event(
    drift_type,
    severity,
    region,
    segment,
    description,
    governance_exposure,
    operational_impact,
    escalation_required
):

    governance_events.append({

        "drift_type":
            drift_type,

        "severity":
            severity,

        "region":
            region,

        "segment":
            segment,

        "description":
            description,

        "governance_exposure":
            governance_exposure,

        "operational_impact":
            operational_impact,

        "escalation_required":
            escalation_required
    })

for _, row in df.iterrows():

    region = row["region"]

    segment = row["segment"]

    total_net_flow = row["total_net_flow"]

    total_txn_count = row["total_txn_count"]

    avg_net_flow = row["avg_net_flow"]

    if total_net_flow < 100000:

        register_governance_event(
            drift_type="LIQUIDITY_GOVERNANCE_DRIFT",
            severity="HIGH",
            region=region,
            segment=segment,
            description=(
                "Detected sustained liquidity deterioration "
                "within institutional banking operations."
            ),
            governance_exposure=(
                "Potential treasury oversight escalation."
            ),
            operational_impact=(
                "Potential operational banking instability."
            ),
            escalation_required=True
        )

    if total_txn_count > 60000:

        register_governance_event(
            drift_type="TRANSACTION_OBSERVABILITY_DRIFT",
            severity="MEDIUM",
            region=region,
            segment=segment,
            description=(
                "Detected elevated transaction observability "
                "pressure within banking infrastructure."
            ),
            governance_exposure=(
                "Operational monitoring review recommended."
            ),
            operational_impact=(
                "Potential banking infrastructure strain."
            ),
            escalation_required=False
        )

    if avg_net_flow < 500:

        register_governance_event(
            drift_type="OPERATIONAL_EFFICIENCY_DRIFT",
            severity="MEDIUM",
            region=region,
            segment=segment,
            description=(
                "Detected operational banking efficiency "
                "deterioration indicators."
            ),
            governance_exposure=(
                "Operational effectiveness review advised."
            ),
            operational_impact=(
                "Potential institutional productivity weakness."
            ),
            escalation_required=False
        )

    if (
        region == "East" and
        total_net_flow > 5000000
    ):

        register_governance_event(
            drift_type="REGIONAL_CONCENTRATION_GOVERNANCE_RISK",
            severity="HIGH",
            region=region,
            segment=segment,
            description=(
                "Detected elevated regional liquidity "
                "concentration dependency."
            ),
            governance_exposure=(
                "Executive concentration governance "
                "oversight recommended."
            ),
            operational_impact=(
                "Potential systemic regional dependency risk."
            ),
            escalation_required=True
        )

governance_context = json.dumps(
    governance_events,
    indent=2
)

PROMPT = f"""
You are the Chief Governance Intelligence Officer of ESOTERIC BANK.

You are operating inside an AI-native enterprise banking governance cognition platform responsible for:
- governance observability
- institutional oversight intelligence
- treasury governance analysis
- operational integrity monitoring
- banking resilience governance
- AI-augmented governance cognition
- executive governance reporting
- institutional operational oversight
- enterprise banking observability

Analyze the following governance cognition dataset.

Generate an enterprise-grade governance intelligence briefing suitable for:
- executive governance boards
- treasury governance committees
- institutional oversight leadership
- enterprise operational governance
- banking audit leadership
- AI governance divisions
- executive banking leadership
- strategic operational governance teams

The report must contain:

1. Executive Governance Intelligence Summary
2. Governance Drift Analysis
3. Treasury Governance Exposure
4. Banking Operational Integrity Assessment
5. Governance Escalation Priorities
6. Institutional Stability Commentary
7. Operational Governance Weaknesses
8. Enterprise Oversight Observations
9. Governance Resilience Assessment
10. Executive Oversight Recommendations
11. Predictive Governance Exposure Analysis
12. Banking Operational Stability Outlook
13. AI-Augmented Governance Opportunities
14. Institutional Governance Modernization Recommendations
15. Strategic Governance Intelligence Assessment

The analysis should:
- identify institutional governance weaknesses
- explain operational integrity concerns
- infer treasury governance exposure
- identify observability degradation
- explain executive oversight implications
- assess banking governance resilience
- emulate enterprise governance committee reporting
- provide institutional governance commentary

The tone must be:
- executive-grade
- governance-aware
- audit-conscious
- operationally analytical
- technically authoritative
- institutionally aligned
- strategically rigorous

Critical Rules:
- Do not mention SQL
- Do not explain methodology
- Do not simplify governance terminology
- Avoid generic commentary
- Focus on institutional governance resilience
- Provide enterprise-grade strategic governance interpretation

Output professional markdown only.

GOVERNANCE COGNITION DATASET:
====================================================================

{governance_context}
"""

result = subprocess.run(
    ["gemini", "-p", PROMPT],
    capture_output=True,
    text=True
)

REPORT_FILE.write_text(result.stdout)

print(f"\nGovernance cognition report generated:")
print(REPORT_FILE)

SUMMARY = """
====================================================================
AUTONOMOUS GOVERNANCE COGNITION COMPLETE
====================================================================

ESOTERIC BANK now supports:
- institutional governance cognition
- operational governance observability
- executive oversight intelligence
- treasury governance analysis
- AI-native governance resilience monitoring
- autonomous operational governance intelligence
- enterprise institutional oversight cognition

====================================================================
"""

print(SUMMARY)
