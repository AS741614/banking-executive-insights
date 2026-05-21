# Executive Demo Walkthrough: Institutional Intelligence Cycle

This document provides a guided walkthrough for demonstrating the full cognitive lifecycle of the ESOTERIC BANK platform.

---

## Scenario 1: The Regulatory Escalation Cycle

### Objective
Demonstrate how the platform autonomously detects, orchestrates, and visualizes a critical compliance failure.

### Steps
1.  **Dashboard Access**: Navigate to `http://localhost:3000/governance`. Observe the `SYNCHRONIZED` posture.
2.  **Trigger Injection**: Use the **Executive Scenario Console** (bottom right). Click **"High-Risk KYC Injection"**.
3.  **Real-time Reaction**:
    - Observe the **Institutional Incident Timeline** animate. A `CRITICAL` escalation appears instantly.
    - Notice the **Governance Posture** card transition to `DEGRADED` (Red border pulse).
    - Watch the **KYC Topology** pie chart update its distribution.
4.  **Audit Verification**: Navigate to the terminal or API logs. Observe the `InstitutionalAuditLogger` recording the transition with a cryptographic checksum.

---

## Scenario 2: Institutional Governance Drift

### Objective
Demonstrate the platform's ability to monitor domain-specific policy variance.

### Steps
1.  **Trigger Injection**: In the Scenario Console, click **"Governance Drift Spike"**.
2.  **Real-time Reaction**:
    - The dashboard captures the `GOVERNANCE_DRIFT_DETECTED` event.
    - An **Operational Realignment** note appears, detailing the ECOS kernel's response to the variance.
    - The **Compliance Score** reflects the real-time institutional drift index.

---

## Scenario 3: AI-Native Copilot Intelligence

### Objective
Demonstrate institutional intelligence querying with governance guardrails.

### Steps
1.  **Access**: Navigate to `http://localhost:3000/copilot`.
2.  **Query**: Enter an institutional query: *"Analyze capital adequacy sensitivity for Sector 7."*
3.  **Observation**:
    - Observe the **Processing_Cognitive_Trace** loading state.
    - Review the **Confidence Score** and **Source Attribution** in the response.
    - Note the **Audit Trace Panel** tracking the query's path through the governance reconciliation engine.

---

## Scenario 4: Platform Observability & Telemetry

### Objective
Demonstrate the underlying infrastructure health and trace continuity.

### Steps
1.  **Access**: Navigate to `http://localhost:3000/observability`.
2.  **Verification**:
    - Verify the **Event Stream: Online** badge.
    - Observe the **API Latency Tracing** chart (hardened Recharts).
    - Monitor the **Cognitive Event Ticker** as it captures every internal signal from previous scenarios.
3.  **Deep Dive**: Click the **"GRAFANA_CORE"** link to view the auto-provisioned executive oversight dashboards.
