# ESOTERIC BANK - Executive Copilot Conversational Architecture

This domain provides the high-fidelity conversational interface for institutional intelligence.

### 1. Conversational Reasoning Engine (`ai/executive/copilot/engine.py`)
- **Intent Classification**: Identifies if the executive is asking for KPI explanations, governance Q&A, or strategic recommendations.
- **Context Retrieval**: Links conversational queries to intelligence datasets and institutional state.
- **Explainable Reasoning**: Formulates responses that prioritize transparency and institutional data-backed analysis.

### 2. Institutional Persona & Prompts (`ai/executive/copilot/prompts.py`)
- Defines the authoritative, senior-advisor persona for the copilot.
- Enforces institutional tone and safety standards in every generated response.

### 3. Governance Layer (`ai/executive/copilot/governance.py`)
- **Sanitization**: Prevents processing of queries containing restricted terms or PII.
- **Leakage Prevention**: Validates assistant responses to ensure no sensitive institutional secrets are exposed.
- **Policy Enforcement**: Rejects requests that would violate established institutional governance frameworks.

### 4. Executive Console (`ui/pages/copilot_console.py`)
- Immersive Streamlit-based chat interface optimized for executive command centers.
- Features real-time reasoning spinners, cognitive context expanders, and institutional status awareness.
- Provides specialized sidebar tools for controlling the copilot's intelligence domains.
