# ESOTERIC BANK Executive Intelligence Command Center

Institutional-grade visualization platform for executive intelligence, governance monitoring, and compliance observability.

## Architecture
- **Framework**: Streamlit
- **Theme**: Enterprise Dark (Bloomberg-inspired)
- **Integration**: FastAPI Platform Gateway
- **Modularity**: Component-based UI structure

## Setup & Execution

1. **Install UI Dependencies**
   ```bash
   pip install streamlit pandas numpy plotly requests
   ```

2. **Ensure Backend is Running**
   The UI communicates with the FastAPI backend. Ensure it is active:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

3. **Launch the Command Center**
   Use the stabilized startup script from the project root:
   ```bash
   ./ui/run_ui.sh
   ```
   Alternatively, run manually:
   ```bash
   streamlit run ui/main.py
   ```

## Runtime Validation
You can validate your local environment using the included utility:
```bash
python3 ui/validate_runtime.py
```

## Command Domains
- **Executive Overview**: Institutional health metrics, treasury performance, and regulatory escalations.
- **Compliance Center**: AML surveillance, KYC customer risk mapping, and fraud intelligence.
- **Platform Observability**: Real-time infrastructure health and cognitive engine metrics.
- **AI Copilot Console**: Direct interface for institutional intelligence querying.
