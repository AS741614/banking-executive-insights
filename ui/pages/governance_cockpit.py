import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from ui.components.theme import render_institutional_header

def render_governance_cockpit():
    render_institutional_header("Institutional Governance Cockpit")
    
    # --- TOPOLOGY & CONTINUITY ---
    left_col, right_col = st.columns([7, 3])
    
    with left_col:
        st.markdown('<div class="hud-panel"><div class="hud-panel-title">Institutional Organizational Topology</div>', unsafe_allow_html=True)
        
        # Create a synthetic topology map using Plotly
        # Nodes: Core, Regional Hubs, Edge Nodes
        nodes_x = [0, -1, 1, -1.5, -0.5, 0.5, 1.5]
        nodes_y = [0, -1, -1, -2, -2, -2, -2]
        labels = ["INSTITUTIONAL_CORE", "AMER_HUB", "EMEA_HUB", "NY_NODE", "SF_NODE", "LONDON_NODE", "FRANKFURT_NODE"]
        colors = ["#00FF41", "#FFD700", "#FFD700", "#F0F6FC", "#F0F6FC", "#F0F6FC", "#F0F6FC"]
        
        edge_x = []
        edge_y = []
        connections = [(0,1), (0,2), (1,3), (1,4), (2,5), (2,6)]
        for start, end in connections:
            edge_x.extend([nodes_x[start], nodes_x[end], None])
            edge_y.extend([nodes_y[start], nodes_y[end], None])
            
        fig = go.Figure()
        # Edges
        fig.add_trace(go.Scatter(x=edge_x, y=edge_y, line=dict(width=1, color='#1B1F24'), hoverinfo='none', mode='lines'))
        # Nodes
        fig.add_trace(go.Scatter(x=nodes_x, y=nodes_y, mode='markers+text', 
                                text=labels, textposition="bottom center",
                                marker=dict(size=20, color=colors, line=dict(width=2, color='#0D1117')),
                                textfont=dict(family="JetBrains Mono", size=10, color="#8B949E")))
        
        fig.update_layout(
            showlegend=False,
            margin=dict(l=0, r=0, t=0, b=0),
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="hud-panel"><div class="hud-panel-title">Policy Drift & Alignment Matrix</div>', unsafe_allow_html=True)
        df_drift = pd.DataFrame({
            "Policy Domain": ["AML_SYNC_V4", "KYC_ENHANCED", "TREASURY_L1_LIQUIDITY", "FRAUD_PRO_SIGNATURES"],
            "Alignment": ["98.2%", "99.1%", "82.4%", "94.8%"],
            "Status": ["OPTIMAL", "OPTIMAL", "CRITICAL_DRIFT", "DEGRADED"],
            "Last Evolution": ["2026-05-10", "2026-05-12", "2026-04-20", "2026-05-15"]
        })
        
        # Display as a styled table
        st.dataframe(df_drift, hide_index=True, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with right_col:
        st.markdown('<div class="hud-panel"><div class="hud-panel-title">Governance Intelligence</div>', unsafe_allow_html=True)
        st.warning("**CRITICAL_DRIFT:** TREASURY_L1_LIQUIDITY mismatch in EMEA segment. Institutional alignment below threshold (85%).")
        st.info("**PROPOSAL:** Adaptive Cognition suggests immediate realignment of regional thresholds to match Global Tier 1 standards.")
        
        if st.button("INITIATE REALIGNMENT", use_container_width=True):
            st.success("Realignment sequence broadcasted to all regional nodes.")
        
        st.markdown("---")
        st.subheader("Evolutionary Roadmap")
        st.markdown("""
        - **Q2_ACTIVATE:** Multi-agent AML sync
        - **Q3_PLAN:** Cognitive Liquidity Engine
        - **Q4_TARGET:** Fully Autonomous Governance
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="hud-panel"><div class="hud-panel-title">Audit Continuity</div>', unsafe_allow_html=True)
        st.metric("Continuous Audit Score", "98.4", "+0.2")
        st.progress(0.98, text="Institutional Integrity")
        st.markdown('</div>', unsafe_allow_html=True)
