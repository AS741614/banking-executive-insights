import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT))

from datetime import datetime
import subprocess
import pandas as pd
from sqlalchemy import text
from sklearn.linear_model import LinearRegression
import numpy as np

from src.db import get_engine

engine = get_engine()

REPORT_DIR = ROOT / "ai/forecasting/reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

REPORT_FILE = REPORT_DIR / f"predictive_banking_intelligence_{timestamp}.md"

HEADER = f"""
====================================================================
ESOTERIC BANK
Predictive Cognitive Banking Intelligence Engine
====================================================================

AI-Native Predictive Banking Observability Platform

Capabilities:
- Predictive Liquidity Intelligence
- Treasury Stability Forecasting
- Enterprise Risk Projection
- Banking Operational Trajectory Analysis
- Governance-Aware Predictive Reporting
- Future-State Banking Intelligence
- Strategic Financial Observability
- Predictive Executive Intelligence

Forecast Intelligence Timestamp:
{timestamp}

====================================================================
"""

print(HEADER)

QUERY = """
SELECT
    dd.year,
    dd.month,

    SUM(fam.net_flow) AS monthly_net_flow,
    SUM(fam.txn_count) AS monthly_txn_count

FROM mart.fact_account_month fam

JOIN mart.dim_date dd
    ON fam.date_key = dd.date_key

GROUP BY
    dd.year,
    dd.month

ORDER BY
    dd.year,
    dd.month;
"""

df = pd.read_sql(text(QUERY), engine)

df["time_index"] = np.arange(len(df))

X = df[["time_index"]]

y = df["monthly_net_flow"]

model = LinearRegression()

model.fit(X, y)

forecast_horizon = 6

future_index = np.arange(
    len(df),
    len(df) + forecast_horizon
).reshape(-1, 1)

future_predictions = model.predict(future_index)

forecast_df = pd.DataFrame({

    "forecast_period":
        range(1, forecast_horizon + 1),

    "predicted_net_flow":
        future_predictions
})

forecast_context = forecast_df.to_markdown(index=False)

PROMPT = f"""
You are the Chief Predictive Intelligence Officer of ESOTERIC BANK.

You are operating inside an AI-native enterprise banking cognition platform responsible for:
- predictive treasury intelligence
- future-state banking observability
- enterprise liquidity forecasting
- governance-aware predictive analysis
- operational banking trajectory interpretation
- strategic financial forecasting
- institutional banking risk projection
- AI-augmented executive forecasting intelligence

Analyze the following predictive banking intelligence dataset.

Generate an enterprise-grade predictive banking intelligence briefing suitable for:
- treasury leadership
- enterprise governance boards
- banking strategy divisions
- executive operational leadership
- institutional risk committees
- AI governance leadership
- financial stability oversight teams

The report must contain:

1. Executive Predictive Intelligence Summary
2. Treasury Liquidity Forecast Interpretation
3. Banking Stability Outlook
4. Predictive Operational Risk Analysis
5. Future-State Governance Exposure
6. Strategic Banking Forecast Commentary
7. Predictive Concentration Risk Analysis
8. Forecasted Operational Banking Conditions
9. Institutional Financial Stability Assessment
10. Emerging Treasury Risk Signals
11. AI-Augmented Predictive Intelligence Opportunities
12. Enterprise Banking Modernization Recommendations
13. Predictive Governance Observability Commentary
14. Strategic Banking Resilience Assessment

The analysis should:
- interpret future banking trajectories
- infer future operational instability
- identify predictive liquidity risks
- explain emerging concentration dependencies
- evaluate future governance pressure
- assess institutional resilience outlook
- emulate executive banking forecasting memoranda
- provide enterprise-grade strategic forecasting commentary

The tone must be:
- executive-grade
- analytically rigorous
- governance-aware
- risk-conscious
- technically authoritative
- institutionally aligned
- strategically analytical

Critical Rules:
- Do not mention SQL
- Do not mention machine learning models
- Do not explain forecasting methodology
- Do not simplify banking terminology
- Avoid generic observations
- Provide strategic institutional commentary
- Focus on observability, governance, and banking stability

Output professional markdown only.

PREDICTIVE BANKING INTELLIGENCE DATASET:
====================================================================

{forecast_context}
"""

result = subprocess.run(
    ["gemini", "-p", PROMPT],
    capture_output=True,
    text=True
)

REPORT_FILE.write_text(result.stdout)

print(f"\nPredictive banking intelligence report generated:")
print(REPORT_FILE)

SUMMARY = """
====================================================================
PREDICTIVE BANKING INTELLIGENCE COMPLETE
====================================================================

ESOTERIC BANK now supports:
- predictive banking cognition
- future-state liquidity intelligence
- treasury trajectory forecasting
- predictive governance observability
- institutional banking forecasting
- AI-native strategic financial prediction
- enterprise operational trajectory analysis

====================================================================
"""

print(SUMMARY)
