# ESOTERIC BANK Fraud Intelligence Domain

Enterprise-grade fraud cognition and financial threat intelligence infrastructure.

## Architecture
- **Framework**: Modular Python Services
- **Detection**: Composite Multi-Factor Fraud Detection
- **Anomaly Detection**: Behavioral Drift & Operational Anomaly Engines
- **Device Intelligence**: Hardware Fingerprinting & Network Risk Analysis
- **Event-Driven**: Integrated with the `CognitiveEventBus` for real-time threat streaming.

## Core Engines

### 1. Fraud Detection Engine (`ai/fraud/engines/fraud_engine.py`)
Synthesizes behavioral signals and device intelligence to classify transaction risk. It identifies patterns like Account Takeover (ATO) and Synthetic Identity fraud.

### 2. Behavioral Anomaly Engine (`ai/fraud/engines/anomaly_engine.py`)
Monitors customer activity against historical baselines to identify velocity variances, geographical drift, and unusual time patterns.

### 3. Device Intelligence Layer (`ai/fraud/engines/device_engine.py`)
Performs technical risk assessment on the originating device, detecting VPNs, proxies, TOR nodes, and emulators.

### 4. Fraud Governance Service (`ai/fraud/services/fraud_governance.py`)
Central orchestrator that executes the fraud cognition cycle and publishes high-fidelity threat intelligence events to the platform's event bus.

## Fraud Cognition Workflow
1. **Ingest**: Transaction and device context are received.
2. **Analyze**: Behavioral and device engines execute in parallel.
3. **Synthesize**: The detection engine computes a composite fraud score and risk level.
4. **Govern**: An institutional action (MONITOR, CHALLENGE, BLOCK) is determined.
5. **Publish**: A `CognitiveEvent` is emitted for downstream executive visibility and operational response.
