import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT))

from datetime import datetime
import time
import pandas as pd
from sqlalchemy import text

from src.db import get_engine

engine = get_engine()

HEADER = """
====================================================================
ESOTERIC BANK
Continuous Cognitive Observability Infrastructure
====================================================================

AI-Native Enterprise Banking Monitoring Layer

Capabilities:
- Continuous Liquidity Surveillance
- Governance Drift Monitoring
- Banking Stability Observability
- Transaction Velocity Monitoring
- Institutional Risk Signaling
- Treasury Exposure Surveillance
- Real-Time Banking Intelligence
- Autonomous Operational Monitoring

====================================================================
"""

print(HEADER)

QUERY = """
WITH institutional_observability AS (

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

SELECT *
FROM institutional_observability;
"""

cycle = 1

while True:

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("\n====================================================================")
    print(f"COGNITIVE OBSERVABILITY CYCLE: {cycle}")
    print(f"TIMESTAMP: {timestamp}")
    print("====================================================================\n")

    df = pd.read_sql(text(QUERY), engine)

    active_alerts = []

    for _, row in df.iterrows():

        region = row["region"]

        segment = row["segment"]

        total_net_flow = row["total_net_flow"]

        total_txn_count = row["total_txn_count"]

        avg_net_flow = row["avg_net_flow"]

        if total_net_flow < 100000:

            active_alerts.append({
                "severity": "HIGH",
                "event": "LIQUIDITY_PRESSURE_SIGNAL",
                "region": region,
                "segment": segment,
                "message":
                    "Detected institutional liquidity "
                    "pressure within banking operations."
            })

        if total_txn_count > 60000:

            active_alerts.append({
                "severity": "MEDIUM",
                "event": "TRANSACTION_VELOCITY_SIGNAL",
                "region": region,
                "segment": segment,
                "message":
                    "Detected elevated transaction "
                    "velocity within banking systems."
            })

        if (
            region == "East" and
            total_net_flow > 5000000
        ):

            active_alerts.append({
                "severity": "HIGH",
                "event": "REGIONAL_CONCENTRATION_SIGNAL",
                "region": region,
                "segment": segment,
                "message":
                    "Detected elevated regional liquidity "
                    "dependency concentration."
            })

        if avg_net_flow < 500:

            active_alerts.append({
                "severity": "MEDIUM",
                "event": "OPERATIONAL_EFFICIENCY_SIGNAL",
                "region": region,
                "segment": segment,
                "message":
                    "Detected operational banking "
                    "efficiency deterioration."
            })

    if active_alerts:

        print("ACTIVE INSTITUTIONAL COGNITIVE SIGNALS\n")

        for alert in active_alerts:

            print(
                f"[{alert['severity']}] "
                f"{alert['event']} "
                f"| Region={alert['region']} "
                f"| Segment={alert['segment']}"
            )

            print(f"→ {alert['message']}\n")

    else:

        print("Institutional systems stable.")
        print("No active governance anomalies detected.\n")

    print("Observability cycle complete.")

    cycle += 1

    time.sleep(10)
