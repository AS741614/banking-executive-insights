# ESOTERIC BANK Executive Demo & Cognitive Experience

Enterprise-grade operational intelligence demonstration environment.

## Architecture
- **Framework**: Scenario-driven orchestration
- **Event-Driven**: Fully integrated with the platform's `CognitiveEventBus`
- **Narrative-Focused**: Designed for executive storytelling and institutional realism
- **Modular**: Reusable scenario and step models

## Core Components

### 1. Scenario Orchestrator (`demo/orchestration/scenario_orchestrator.py`)
The engine responsible for executing `DemoScenario` objects. It simulates operational reality by emitting cognitive and governance events in a timed sequence.

### 2. Scenario Registry (`demo/scenarios/scenario_registry.py`)
A centralized repository of institutional intelligence scenarios, including AML escalations and fraud prevention workflows.

### 3. Scenario Models (`demo/models/scenario_models.py`)
Strict Pydantic models for defining structured operational workflows, including steps, actions, payloads, and governance commentary.

## Execution

To run the full institutional demo sequence:

```bash
python demo/run_demo.py
```

## Demo Scenarios

### Institutional AML Escalation
- **Narrative**: High-velocity anomaly detection leading to executive governance review.
- **Workflow**: Anomaly Detection -> Cross-Domain Analysis -> Executive Escalation -> SAR Recommendation.

### Real-time Fraud Prevention
- **Narrative**: Device intelligence identifying a high-risk session and triggering an automated block.
- **Workflow**: Device Profiling -> Behavioral Synthesis -> Automated Institutional Action.

## Visualization
All demo events are published to the global event bus. When the platform's FastAPI gateway and Streamlit UI are active, the demo sequences will appear in real-time in the **Executive Command Center** (Cognitive Event Stream).
