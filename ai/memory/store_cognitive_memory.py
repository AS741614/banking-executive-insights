from pathlib import Path
from datetime import datetime
import shutil
import json

ROOT = Path(__file__).resolve().parent.parent.parent

GENERATED_DIR = ROOT / "ai/generated"
MEMORY_ROOT = ROOT / "ai/memory"

MEMORY_ROOT.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

SNAPSHOT_DIR = MEMORY_ROOT / f"cognitive_snapshot_{timestamp}"

SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)

REPORTS = [
    {
        "name": "Enterprise Governance Intelligence",
        "file": "esoteric_bank_intelligence_report.md"
    },
    {
        "name": "Executive Banking Intelligence",
        "file": "executive_intelligence_summary.md"
    },
    {
        "name": "Enterprise Risk Intelligence",
        "file": "risk_intelligence_report.md"
    }
]

HEADER = f"""
====================================================================
ESOTERIC BANK
Temporal Cognitive Memory Architecture
====================================================================

Snapshot Timestamp:
{timestamp}

Institutional Memory Classification:
Enterprise Banking Cognitive Snapshot

Memory Domains:
- Governance Intelligence
- Executive Intelligence
- Risk Intelligence
- Operational Banking Observability
- AI-Augmented Strategic Interpretation
- Fraud Intelligence Context
- Longitudinal Banking Cognition

====================================================================
"""

print(HEADER)

metadata = {
    "snapshot_timestamp": timestamp,
    "platform": "ESOTERIC BANK",
    "memory_classification": "Enterprise Cognitive Banking Snapshot",
    "stored_assets": [],
    "missing_assets": [],
    "institutional_memory_status": "ACTIVE"
}

MEMORY_LOG = SNAPSHOT_DIR / "cognitive_memory_log.txt"

with open(MEMORY_LOG, "w") as log:

    log.write(HEADER)

    for report in REPORTS:

        source = GENERATED_DIR / report["file"]

        if source.exists():

            destination = SNAPSHOT_DIR / report["file"]

            shutil.copy(source, destination)

            metadata["stored_assets"].append(report["name"])

            print(f"Stored Cognitive Asset: {report['name']}")

            log.write(
                f"\n[STORED] {report['name']} -> {report['file']}"
            )

        else:

            metadata["missing_assets"].append(report["name"])

            print(f"Missing Cognitive Asset: {report['name']}")

            log.write(
                f"\n[MISSING] {report['name']}"
            )

METADATA_FILE = SNAPSHOT_DIR / "snapshot_metadata.json"

with open(METADATA_FILE, "w") as meta:
    json.dump(metadata, meta, indent=4)

SUMMARY = f"""

====================================================================
COGNITIVE MEMORY SNAPSHOT COMPLETED
====================================================================

Snapshot Directory:
{SNAPSHOT_DIR}

Stored Cognitive Assets:
{len(metadata["stored_assets"])}

Missing Cognitive Assets:
{len(metadata["missing_assets"])}

Institutional Memory Status:
ACTIVE

ESOTERIC BANK now maintains:
- persistent executive cognition
- longitudinal risk intelligence
- governance memory retention
- operational observability history
- temporal banking intelligence continuity
- AI-assisted institutional memory architecture

Strategic Capabilities Enabled:
- longitudinal anomaly comparison
- historical governance tracking
- operational deterioration detection
- risk escalation pattern analysis
- executive intelligence continuity
- institutional banking observability

====================================================================
"""

print(SUMMARY)

with open(MEMORY_LOG, "a") as log:
    log.write(SUMMARY)
