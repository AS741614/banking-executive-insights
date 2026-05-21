# ESOTERIC BANK - Executive Demo Mode Infrastructure

Enterprise-grade institutional simulation and demonstration environment.

## 🚀 Overview
The Executive Demo Mode provides a high-fidelity environment for showcasing the platform's cognitive capabilities, crisis management, and governance resilience. It allows executives to experience real-time institutional responses to complex stress scenarios.

## 🛠 Core Components

### 1. Crisis Trigger Console (`ui/pages/demo_control_center.py`)
A centralized command center for initiating orchestrated scenarios or injecting manual crisis vectors (Liquidity, Fraud, Governance Drift).

### 2. Executive Command Center (`ui/pages/executive_overview.py`)
The primary dashboard for executives, featuring:
- **Real-time KPI Evolution**: Metrics that react to institutional events.
- **Live Cognitive Stream**: A high-density feed of cross-domain intelligence.
- **Executive Walkthrough Mode**: A guided experience with educational overlays and cognitive insights.

### 3. AI Copilot Narration (`ui/pages/copilot_console.py`)
The "Crisis Narration Mode" allows the Institutional Copilot to automatically explain unfolding events and the reasoning behind automated mitigations.

### 4. Institutional Replay Mode (`demo/orchestration/replay_engine.py`)
Enables recording and replaying demo sequences at variable speed factors for post-mortem analysis and presentation consistency.

## 🌪 Available Scenarios

| Scenario | Domain | Objective |
|----------|--------|-----------|
| **Institutional AML Escalation** | Regulatory | Detection -> Cross-Domain Analysis -> Executive Escalation |
| **Real-time Fraud Prevention** | Operational | Device Intelligence -> ATO Detection -> Automated Block |
| **Institutional Governance Escalation** | Governance | Drift Detection -> Mitigation Synthesis -> Board Approval |
| **APAC Liquidity Deterioration** | Treasury | Regional Signal -> KPI Impact -> Automated Rebalancing |

## 🕹 Getting Started

### Running the Full Experience
1. Start the ESOTERIC Backend API:
   ```bash
   uvicorn app.main:app --reload
   ```
2. Launch the Streamlit Executive Interface:
   ```bash
   streamlit run ui/main.py
   ```
3. Navigate to **DEMO_CONTROL_CENTER** to initiate a scenario.

### Developer Tools
- **Crisis Injector**: `testing/final_cascade/crisis_injector.py`
- **Scenario Registry**: `demo/scenarios/scenario_registry.py`
- **Orchestrator**: `demo/orchestration/scenario_orchestrator.py`

---
*ESOTERIC BANK - Proprietary Institutional Intelligence Infrastructure*
