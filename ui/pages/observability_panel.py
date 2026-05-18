import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from ui.components.theme import render_header
from ui.utils.api_client import APIClient

def render_observability_page():
    render_header("Platform Observability")
    
    health_data = APIClient.get_platform_status()
    
    st.subheader("System Health & Infrastructure")
    cols = st.columns(4)
    cols[0].metric("FastAPI Status", health_data.get("status", "OFFLINE"))
    cols[1].metric("Gemini Engine", "ACTIVE", "0.2ms")
    cols[2].metric("Thread Utilization", "12%", "-2%")
    cols[3].metric("Uptime", health_data.get("uptime", "N/A"))

    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("Cognitive Engine Metrics")
        # Mocking some engine metrics
        metrics = {
            "Instruction count": "1.2B",
            "Context Window": "2M Tokens",
            "Active Agents": 14,
            "Queue Depth": 0
        }
        for k, v in metrics.items():
            st.write(f"**{k}:** {v}")
            
        # Mock performance graph
        chart_data = pd.DataFrame(
            np.random.randn(50, 2),
            columns=['Inference Latency (ms)', 'Token Throughput']
        ).cumsum()
        st.line_chart(chart_data)

    with col_right:
        st.subheader("API Integration Health")
        is_connected = APIClient.check_connectivity()
        if is_connected:
            st.success("Successfully connected to ESOTERIC Backend API")
        else:
            st.error("Backend API is currently unreachable. UI is in OFFLINE mode.")
            
        st.subheader("Service Topology")
        # Simple visualization of service status
        services = {
            "Auth Service": "HEALTHY",
            "Cognition Service": "HEALTHY",
            "ETL Pipeline": "DEGRADED",
            "Ontology Engine": "HEALTHY"
        }
        for svc, status in services.items():
            color = "green" if status == "HEALTHY" else "orange"
            st.markdown(f"- **{svc}**: :{color}[{status}]")
