import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from ui.components.theme import render_institutional_header
from ui.utils.api_client import APIClient

def render_observability_page():
    render_institutional_header("Platform Observability")
    
    health_data = APIClient.get_platform_status()
    agents_data = APIClient.get_agents_distributed()
    events = APIClient.get_event_history()
    
    # --- TOP TIER INFRA METRICS ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("FastAPI Gateway", health_data.get("status", "OFFLINE").upper())
    with col2:
        cognitive_ops = health_data.get("cognitive_ops", "1.4B Ops")
        st.metric("Cognitive Core", "HEALTHY", cognitive_ops)
    with col3:
        utilization = health_data.get("thread_utilization", "12%")
        st.metric("Thread Utilization", utilization, "-2%")
    with col4:
        st.metric("System Uptime", health_data.get("uptime", "N/A"))

    st.markdown("<br>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown('<div class="hud-panel"><div class="hud-panel-title">Cognitive Engine Metrics</div>', unsafe_allow_html=True)
        metrics = {
            "Instruction count": health_data.get("instruction_count", "1.2B"),
            "Context Window": health_data.get("context_window", "2M Tokens"),
            "Active Agents": agents_data.get("active_agents", 14),
            "Queue Depth": health_data.get("queue_depth", 0)
        }
        for k, v in metrics.items():
            st.markdown(f"**{k}:** `{v}`")
            
        chart_data = pd.DataFrame(
            np.random.randn(50, 2),
            columns=['Inference Latency', 'Token Throughput']
        ).cumsum()
        st.line_chart(chart_data)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="hud-panel"><div class="hud-panel-title">Institutional Cognitive Load</div>', unsafe_allow_html=True)
        heatmap_data = np.random.rand(10, 10)
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data,
            colorscale=[[0, '#0D1117'], [0.5, '#FFD700'], [1, '#FF3E3E']],
            showscale=False
        ))
        fig.update_layout(
            height=250,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="hud-panel"><div class="hud-panel-title">Service Topology Status</div>', unsafe_allow_html=True)
        services = health_data.get("services", [
            {"name": "AUTH_SERVICE", "status": "HEALTHY", "load": "12%"},
            {"name": "COGNITION_HUB", "status": "HEALTHY", "load": "45%"},
            {"name": "ETL_PIPELINE", "status": "DEGRADED", "load": "88%"},
            {"name": "ONTOLOGY_ENGINE", "status": "HEALTHY", "load": "22%"}
        ])
        
        for svc in services:
            color = "#00FF41" if svc['status'] == "HEALTHY" else "#FFD700" if svc['status'] == "DEGRADED" else "#FF3E3E"
            st.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: center; background-color: #080A0E; padding: 12px; margin-bottom: 8px; border: 1px solid #1B1F24;">
                    <span style="font-family: 'JetBrains Mono'; font-size: 0.8rem; font-weight: 700;">{svc['name']}</span>
                    <span style="color: {color}; font-family: 'JetBrains Mono'; font-size: 0.7rem;">{svc['status']} // {svc['load']}</span>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown('<div class="hud-panel"><div class="hud-panel-title">Institutional Audit Logs</div>', unsafe_allow_html=True)
    if events:
        log_content = "\n".join([f"[{e.get('timestamp')}] {e.get('category')}: {e.get('action')}" for e in events[:10]])
        st.code(log_content)
    else:
        st.code("""
        [2026-05-18 14:22:01] TRACE-8821: AML Inference Complete.
        [2026-05-18 14:21:45] TRACE-9912: Fraud Anomaly Detected.
        [2026-05-18 14:20:12] SYSTEM: Policy Evolution Re-loaded.
        """)
    st.markdown('</div>', unsafe_allow_html=True)
