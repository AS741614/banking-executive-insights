import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from ui.components.theme import render_institutional_header

def render_executive_dashboard():
    render_institutional_header("Executive Command Center")
    
    # --- TOP TIER COCKPIT ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Institutional AUM", "$4.82T", "+0.45%")
    with col2:
        st.metric("Governance Drift", "0.04%", "-0.01%", delta_color="inverse")
    with col3:
        st.metric("Cognitive Load", "12.4K TPM", "+1.2K")
    with col4:
        st.metric("System Resilience", "99.999%", "STABLE")

    st.markdown("### Operational Continuity & Risk Analysis")
    
    # --- MAIN ANALYTICS SECTION ---
    left_col, right_col = st.columns([7, 3])
    
    with left_col:
        # High-density chart: Treasury Performance
        st.subheader("Treasury Performance & Liquidity Heatmap")
        
        # Using numpy to generate realistic-looking synthetic data
        months = pd.date_range(start='2026-01-01', periods=12, freq='M')
        data = pd.DataFrame({
            'Month': months,
            'Tier 1 Capital': 100 + np.random.randn(12).cumsum(),
            'Liquidity': 85 + np.random.randn(12).cumsum(),
            'Risk Exposure': 20 + np.random.randn(12).cumsum()
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Month'], y=data['Tier 1 Capital'], name='Tier 1 Capital', line=dict(color='#00FF41', width=3)))
        fig.add_trace(go.Scatter(x=data['Month'], y=data['Liquidity'], name='Liquidity', line=dict(color='#FFD700', width=2, dash='dot')))
        fig.add_trace(go.Scatter(x=data['Month'], y=data['Risk Exposure'], name='Risk Exposure', line=dict(color='#FF3E3E', width=2)))
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#8B949E',
            margin=dict(l=0, r=0, t=20, b=0),
            height=350,
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=True, gridcolor='#1B1F24', zeroline=False),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Regional Governance Status")
        st.table(pd.DataFrame({
            "Jurisdiction": ["EMEA", "AMER", "APAC", "LATAM"],
            "Operational Tier": ["TIER_1", "TIER_1", "TIER_3_ESCALATED", "TIER_2"],
            "Compliance Score": ["99.8%", "98.5%", "84.2%", "94.6%"],
            "Drift Index": ["0.01", "0.05", "0.28", "0.08"],
            "Last Audit": ["STABLE", "STABLE", "WARNING", "STABLE"]
        }))

    with right_col:
        st.subheader("Live Cognitive Stream")
        # Event Stream Simulation
        events = [
            {"time": "14:22:01", "cat": "AML", "msg": "Large block detected: APAC-CLUSTER-9", "sev": "HIGH"},
            {"time": "14:21:45", "cat": "FRAUD", "msg": "Emulator signature match blocked.", "sev": "CRITICAL"},
            {"time": "14:20:12", "cat": "GOV", "msg": "Policy evolution recommended: KYC-V4", "sev": "INFO"},
            {"time": "14:18:55", "cat": "OPS", "msg": "Node synchronization complete.", "sev": "INFO"},
            {"time": "14:15:33", "cat": "REG", "msg": "SAR Filing auto-drafted: CASE-8821", "sev": "MEDIUM"}
        ]
        
        for e in events:
            color = "#00FF41" if e['sev'] == "INFO" else "#FFD700" if e['sev'] == "MEDIUM" else "#FF3E3E"
            st.markdown(f"""
                <div style="background-color: #0D1117; border-left: 4px solid {color}; padding: 10px; margin-bottom: 10px; border-radius: 0 4px 4px 0;">
                    <div style="font-size: 0.7rem; color: #8B949E;">{e['time']} // {e['cat']}</div>
                    <div style="font-size: 0.85rem; font-weight: 600;">{e['msg']}</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("Executive Actions")
        if st.button("APPROVE GOVERNANCE EVOLUTION: KYC-V4", use_container_width=True):
            st.success("Evolution Proposal Transmitted to Board.")
        if st.button("TRIGGER INSTITUTIONAL AUDIT REPLAY", use_container_width=True):
            st.warning("Audit Replay Initialized for APAC Segment.")
