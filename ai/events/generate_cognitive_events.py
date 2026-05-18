import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT))

from datetime import datetime
import json
import pandas as pd
from sqlalchemy import text

from src.db import get_engine

engine = get_engine()

EVENT_DIR = ROOT / "ai/events/generated"
EVENT_DIR.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

EVENT_FILE = EVENT_DIR / f"cognitive_events_{timestamp}.json"

HEADER = f"""
====================================================================
ESOTERIC BANK
Enterprise Cognitive Event Intelligence Bus
====================================================================

AI-Native Banking Event Architecture

Capabilities:
- Autonomous Risk Signaling
- Liquidity Event Detection
- Governance Escalation Monitoring
- Fraud Intelligence Triggering
- Transaction Velocity Observability
- Operational Banking Event Cognition
- Executive Escalation Signaling
- Regional Concentration Monitoring
- Institutional Banking Observability

Event Generation Timestamp:
{timestamp}

====================================================================
"""

print(HEADER)

QUERY = """
WITH banking_observability AS (

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
FROM banking_observability
ORDER BY total_net_flow DESC;
"""

df = pd.read_sql(text(QUERY), engine)

events = []

def emit_event(
    event_type,
    severity,
    region,
    segment,
    description,
    governance_impact,
    operational_impact,
    escalation_required
):

    events.append({

        "event_id":
            f"{event_type}_{region}_{segment}_{timestamp}",

        "event_type":
            event_type,

        "severity":
            severity,

        "region":
            region,

        "segment":
            segment,

        "description":
            description,

        "governance_impact":
            governance_impact,

        "operational_impact":
            operational_impact,

        "escalation_required":
            escalation_required,

        "event_timestamp":
            timestamp
    })

for _, row in df.iterrows():

    region = row["region"]
    segment = row["segment"]

    net_flow = row["total_net_flow"]
    txn_count = row["total_txn_count"]

    if net_flow < 100000:

        emit_event(
            event_type="LIQUIDITY_PRESSURE_EVENT",
            severity="HIGH",
            region=region,
            segment=segment,
            description=(
                "Detected sustained liquidity weakness "
                "within banking operational segment."
            ),
            governance_impact=(
                "Potential treasury monitoring escalation "
                "required."
            ),
            operational_impact=(
                "Potential regional operational instability."
            ),
            escalation_required=True
        )

    if txn_count > 50000:

        emit_event(
            event_type="HIGH_TRANSACTION_VELOCITY_EVENT",
            severity="MEDIUM",
            region=region,
            segment=segment,
            description=(
                "Elevated transaction activity detected "
                "within operational banking flows."
            ),
            governance_impact=(
                "Fraud observability review recommended."
            ),
            operational_impact=(
                "Potential infrastructure load increase."
            ),
            escalation_required=False
        )

    if (
        net_flow > 5000000 and
        region == "East"
    ):

        emit_event(
            event_type="REGIONAL_CONCENTRATION_RISK_EVENT",
            severity="HIGH",
            region=region,
            segment=segment,
            description=(
                "Detected elevated regional liquidity "
                "concentration dependency."
            ),
            governance_impact=(
                "Executive concentration risk oversight "
                "recommended."
            ),
            operational_impact=(
                "Potential systemic regional dependency."
            ),
            escalation_required=True
        )

    if (
        txn_count < 1000 and
        net_flow < 150000
    ):

        emit_event(
            event_type="OPERATIONAL_ACTIVITY_SUPPRESSION_EVENT",
            severity="MEDIUM",
            region=region,
            segment=segment,
            description=(
                "Suppressed banking activity detected "
                "within regional operations."
            ),
            governance_impact=(
                "Operational effectiveness review advised."
            ),
            operational_impact=(
                "Potential regional market underperformance."
            ),
            escalation_required=False
        )

with open(EVENT_FILE, "w") as file:
    json.dump(events, file, indent=4)

print(f"Generated Cognitive Events: {len(events)}\n")

for event in events:

    print(
        f"[{event['severity']}] "
        f"{event['event_type']} "
        f"| {event['region']} "
        f"| {event['segment']}"
    )

SUMMARY = f"""

====================================================================
COGNITIVE EVENT GENERATION COMPLETE
====================================================================

Generated Event File:
{EVENT_FILE}

Generated Event Count:
{len(events)}

Autonomous Intelligence Categories:
- Liquidity Pressure Events
- Fraud Observability Signals
- Regional Concentration Risks
- Governance Escalation Triggers
- Transaction Velocity Alerts
- Banking Operational Suppression Signals

ESOTERIC BANK now supports:
- event-driven banking cognition
- autonomous governance escalation
- institutional observability signaling
- operational banking intelligence events
- AI-native anomaly detection workflows
- enterprise cognitive risk signaling

====================================================================
"""

print(SUMMARY)
