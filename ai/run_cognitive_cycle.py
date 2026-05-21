import subprocess
from pathlib import Path
from datetime import datetime
import time

ROOT = Path(__file__).resolve().parent.parent

LOG_DIR = ROOT / "ai/logs"
REPORT_DIR = ROOT / "ai/generated"

LOG_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

LOG_FILE = LOG_DIR / f"esoteric_cognitive_cycle_{timestamp}.log"

COGNITIVE_STEPS = [

    {
        "name": "Enterprise Banking Data Generation",
        "description": "Generating operational banking intelligence datasets",
        "command": ["python", "src/generate_source_data.py"]
    },

    {
        "name": "Enterprise Warehouse Synchronization",
        "description": "Executing cognitive ETL synchronization pipelines",
        "command": ["python", "src/etl.py"]
    },

    {
        "name": "Governance & Data Quality Validation",
        "description": "Executing enterprise observability and governance validation",
        "command": ["python", "src/run_quality_checks.py"]
    },

    {
        "name": "AI Governance Intelligence Generation",
        "description": "Generating autonomous banking governance documentation",
        "command": ["python", "ai/generate_docs.py"]
    },

    {
        "name": "Executive Cognitive Intelligence Generation",
        "description": "Generating executive banking observability briefings",
        "command": ["python", "ai/generate_executive_summary.py"]
    },

    {
        "name": "Enterprise Risk Intelligence Generation",
        "description": "Generating fraud observability and risk cognition reports",
        "command": ["python", "ai/generate_risk_intelligence.py"]
    },

    {
        "name": "Tableau Cognitive Intelligence Automation",
        "description": "Synchronizing executive Tableau dashboards and KPI intelligence",
        "command": ["python", "ai/tableau/run_tableau_automation.py"]
    }
]

HEADER = """
============================================================
ESOTERIC BANK
Cognitive Banking Intelligence Orchestration Layer
============================================================

Platform Capabilities:
- Enterprise Banking ETL Synchronization
- Governance Observability
- Executive Intelligence Automation
- AI-Augmented Risk Intelligence
- Fraud Observability
- Cognitive Banking Reporting
- Autonomous Documentation Intelligence
- Enterprise Operational Analytics
- Tableau KPI & Dashboard Orchestration

============================================================
"""

print(HEADER)

with open(LOG_FILE, "w") as log:

    log.write(HEADER)

    cycle_start = datetime.now()

    log.write(f"\nCycle Start Time: {cycle_start}\n")

    for step in COGNITIVE_STEPS:

        separator = "\n" + "=" * 60 + "\n"

        print(separator)
        print(f"STEP: {step['name']}")
        print(f"DESCRIPTION: {step['description']}")
        print("=" * 60)

        log.write(separator)
        log.write(f"STEP: {step['name']}\n")
        log.write(f"DESCRIPTION: {step['description']}\n")

        step_start = time.time()

        result = subprocess.run(
            step["command"],
            cwd=ROOT,
            capture_output=True,
            text=True
        )

        duration = round(time.time() - step_start, 2)

        print(result.stdout)

        log.write(result.stdout)
        log.write(result.stderr)

        log.write(f"\nExecution Time: {duration} seconds\n")

        if result.returncode != 0:

            ERROR_BLOCK = f"""
============================================================
COGNITIVE ORCHESTRATION FAILURE DETECTED
============================================================

FAILED STEP:
{step['name']}

ERROR DETAILS:
{result.stderr}

Immediate governance review recommended.

============================================================
"""

            print(ERROR_BLOCK)

            log.write(ERROR_BLOCK)

            break

SUCCESS_BLOCK = f"""
============================================================
ESOTERIC Cognitive Banking Cycle Completed Successfully
============================================================

Generated Intelligence Assets:
- Governance Documentation
- Executive Intelligence Briefings
- Enterprise Risk Intelligence Reports
- Banking Observability Logs
- AI-Augmented Governance Outputs
- Synchronized Tableau Analytics

Execution Log:
{LOG_FILE}

Generated Reports Directory:
{REPORT_DIR}

============================================================
"""

print(SUCCESS_BLOCK)

with open(LOG_FILE, "a") as log:
    log.write(SUCCESS_BLOCK)
