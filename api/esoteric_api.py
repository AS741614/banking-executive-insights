from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pathlib import Path
from datetime import datetime
import json

ROOT = Path(__file__).resolve().parent.parent

app = FastAPI(
    title="ESOTERIC BANK Cognitive Intelligence Gateway",
    description="""
AI-Native Enterprise Banking Intelligence Platform

Capabilities:
- Executive Banking Intelligence
- Governance Cognition
- Risk Intelligence
- Predictive Banking Intelligence
- Event-Driven Banking Observability
- Distributed Cognitive Orchestration
- Institutional Banking Monitoring
""",
    version="2.0.0"
)

# ============================================================
# PATH CONFIGURATION
# ============================================================

GENERATED_DIR = ROOT / "ai/generated"

EVENT_DIR = ROOT / "ai/events/generated"

FORECAST_DIR = ROOT / "ai/forecasting/reports"

GOVERNANCE_DIR = ROOT / "ai/governance/reports"

AGENT_DIR = ROOT / "ai/agents/reports"

MEMORY_DIR = ROOT / "ai/memory"

# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def latest_file(directory, pattern):

    files = sorted(
        directory.glob(pattern),
        reverse=True
    )

    return files[0] if files else None


def safe_read(file_path):

    try:

        return file_path.read_text()

    except Exception as e:

        return f"Error reading file: {str(e)}"


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():

    return JSONResponse({

        "platform":
            "ESOTERIC BANK",

        "platform_type":
            "AI-Native Enterprise Cognitive Banking Platform",

        "status":
            "OPERATIONAL",

        "timestamp":
            datetime.now().isoformat(),

        "capabilities": [

            "Executive Intelligence",
            "Risk Intelligence",
            "Governance Cognition",
            "Predictive Intelligence",
            "Event Intelligence",
            "Distributed Cognition",
            "Real-Time Observability",
            "Temporal Cognitive Memory"
        ]
    })


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    return JSONResponse({

        "platform_status":
            "HEALTHY",

        "cognitive_status":
            "ACTIVE",

        "observability_status":
            "MONITORING",

        "timestamp":
            datetime.now().isoformat(),

        "active_layers": {

            "executive_intelligence": True,
            "risk_intelligence": True,
            "governance_cognition": True,
            "predictive_intelligence": True,
            "event_intelligence": True,
            "distributed_cognition": True,
            "memory_architecture": True
        }
    })


# ============================================================
# EXECUTIVE INTELLIGENCE
# ============================================================

@app.get("/executive-intelligence")
def executive_intelligence():

    file = GENERATED_DIR / "executive_intelligence_summary.md"

    if file.exists():

        return JSONResponse({

            "report_type":
                "Executive Intelligence",

            "generated_at":
                datetime.now().isoformat(),

            "content":
                safe_read(file)
        })

    return JSONResponse(
        {"error": "Executive intelligence unavailable."},
        status_code=404
    )


# ============================================================
# RISK INTELLIGENCE
# ============================================================

@app.get("/risk-intelligence")
def risk_intelligence():

    file = GENERATED_DIR / "risk_intelligence_report.md"

    if file.exists():

        return JSONResponse({

            "report_type":
                "Enterprise Risk Intelligence",

            "generated_at":
                datetime.now().isoformat(),

            "content":
                safe_read(file)
        })

    return JSONResponse(
        {"error": "Risk intelligence unavailable."},
        status_code=404
    )


# ============================================================
# GOVERNANCE COGNITION
# ============================================================

@app.get("/governance-cognition")
def governance_cognition():

    report = latest_file(
        GOVERNANCE_DIR,
        "*.md"
    )

    if report:

        return JSONResponse({

            "report_type":
                "Governance Cognition",

            "generated_at":
                datetime.now().isoformat(),

            "content":
                safe_read(report)
        })

    return JSONResponse(
        {"error": "Governance cognition unavailable."},
        status_code=404
    )


# ============================================================
# PREDICTIVE INTELLIGENCE
# ============================================================

@app.get("/predictive-intelligence")
def predictive_intelligence():

    report = latest_file(
        FORECAST_DIR,
        "*.md"
    )

    if report:

        return JSONResponse({

            "report_type":
                "Predictive Banking Intelligence",

            "generated_at":
                datetime.now().isoformat(),

            "content":
                safe_read(report)
        })

    return JSONResponse(
        {"error": "Predictive intelligence unavailable."},
        status_code=404
    )


# ============================================================
# EVENT INTELLIGENCE
# ============================================================

@app.get("/event-intelligence")
def event_intelligence():

    report = latest_file(
        EVENT_DIR,
        "*.json"
    )

    if report:

        with open(report) as f:

            events = json.load(f)

        return JSONResponse({

            "event_type":
                "Cognitive Banking Events",

            "generated_at":
                datetime.now().isoformat(),

            "event_count":
                len(events),

            "events":
                events
        })

    return JSONResponse(
        {"error": "Event intelligence unavailable."},
        status_code=404
    )


# ============================================================
# DISTRIBUTED COGNITION
# ============================================================

@app.get("/distributed-cognition")
def distributed_cognition():

    report = latest_file(
        AGENT_DIR,
        "*.md"
    )

    if report:

        return JSONResponse({

            "report_type":
                "Distributed Multi-Agent Cognition",

            "generated_at":
                datetime.now().isoformat(),

            "content":
                safe_read(report)
        })

    return JSONResponse(
        {"error": "Distributed cognition unavailable."},
        status_code=404
    )


# ============================================================
# TEMPORAL MEMORY
# ============================================================

@app.get("/cognitive-memory")
def cognitive_memory():

    snapshots = sorted(
        MEMORY_DIR.glob("*"),
        reverse=True
    )

    return JSONResponse({

        "memory_status":
            "ACTIVE",

        "snapshot_count":
            len(snapshots),

        "latest_snapshots":
            [s.name for s in snapshots[:10]]
    })


# ============================================================
# PLATFORM OBSERVABILITY
# ============================================================

@app.get("/platform-observability")
def platform_observability():

    return JSONResponse({

        "platform":
            "ESOTERIC BANK",

        "observability_status":
            "ACTIVE",

        "operational_state":
            "MONITORING",

        "cognitive_layers": {

            "governance": "ACTIVE",
            "risk": "ACTIVE",
            "forecasting": "ACTIVE",
            "events": "ACTIVE",
            "memory": "ACTIVE",
            "distributed_agents": "ACTIVE"
        },

        "timestamp":
            datetime.now().isoformat()
    })
