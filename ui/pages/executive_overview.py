import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from ui.components.theme import render_institutional_header
from ui.utils.api_client import APIClient

def render_executive_dashboard():
    # --- EXECUTIVE WALKTHROUGH MODE ---
    walkthrough_mode = st.sidebar.toggle("EXECUTIVE WALKTHROUGH MODE", value=False)
    
    if walkthrough_mode:
        st.info("💡 **WALKTHROUGH ACTIVE:** Highlighting key institutional metrics and cognitive reasoning points.")

    render_institutional_header("Executive Command Center")
    
    # --- TOP TIER COCKPIT ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Institutional AUM", "$4.82T", "+0.45%")
        if walkthrough_mode:
            st.caption("Total assets under management across all regional clusters.")
    with col2:
        st.metric("Governance Drift", "0.04%", "-0.01%", delta_color="inverse")
        if walkthrough_mode:
            st.caption("Real-time variance from institutional policy baselines.")
    with col3:
        st.metric("Cognitive Load", "12.4K TPM", "+1.2K")
        if walkthrough_mode:
            st.caption("Transactions processed by the multi-agent reasoning layer.")
    with col4:
        st.metric("System Resilience", "99.999%", "STABLE")
        if walkthrough_mode:
            st.caption("Aggregated health score of all critical infrastructure components.")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- MAIN ANALYTICS SECTION ---
    left_col, right_col = st.columns([7, 3])
    
    with left_col:
        # HUD Panel: Treasury Performance
        st.markdown('<div class="hud-panel"><div class="hud-panel-title">Treasury Performance & Liquidity Velocity</div>', unsafe_allow_html=True)
        
        months = pd.date_range(start='2026-01-01', periods=12, freq='M')
        data = pd.DataFrame({
            'Month': months,
            'Tier 1 Capital': 100 + np.random.randn(12).cumsum(),
            'Liquidity': 85 + np.random.randn(12).cumsum(),
            'Risk Exposure': 20 + np.random.randn(12).cumsum()
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Month'], y=data['Tier 1 Capital'], name='TIER_1_CAPITAL', line=dict(color='#00FF41', width=3), fill='tozeroy', fillcolor='rgba(0, 255, 65, 0.05)'))
        fig.add_trace(go.Scatter(x=data['Month'], y=data['Liquidity'], name='LIQUIDITY_INDEX', line=dict(color='#FFD700', width=2, dash='dot')))
        fig.add_trace(go.Scatter(x=data['Month'], y=data['Risk Exposure'], name='RISK_EXPOSURE', line=dict(color='#FF3E3E', width=2)))
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#8B949E',
            font_family='JetBrains Mono',
            margin=dict(l=0, r=0, t=20, b=0),
            height=300,
            xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(size=10)),
            yaxis=dict(showgrid=True, gridcolor='#1B1F24', zeroline=False, tickfont=dict(size=10)),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=10))
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        if walkthrough_mode:
            st.markdown("""
                <div style="font-size: 0.8rem; color: #8B949E; border-left: 2px solid #FFD700; padding: 10px; background-color: rgba(255, 215, 0, 0.05); margin-bottom: 15px;">
                    <strong>COGNITIVE INSIGHT:</strong> Treasury performance is currently within 1.2% of predicted baseline. 
                    Liquidity velocity remains stable despite regional volatility.
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # HUD Panel: Governance Heatmap
        st.markdown('<div class="hud-panel"><div class="hud-panel-title">Regional Governance Heatmap (Compliance Drift)</div>', unsafe_allow_html=True)
        
        regions = ["NORTH_AMER", "EUROPE_CENTRAL", "ASIA_PACIFIC", "LATAM_SOUTHERN", "MIDDLE_EAST_AFRICA"]
        metrics = ["AML_SYNC", "KYC_DRIFT", "LIQUIDITY_V1", "REG_REPORTING"]
        z_data = np.random.rand(len(regions), len(metrics))
        
        fig_heat = px.imshow(z_data,
                        labels=dict(x="Governance Domain", y="Jurisdiction", color="Risk Level"),
                        x=metrics,
                        y=regions,
                        color_continuous_scale=[[0, '#0D1117'], [0.5, '#FFD700'], [1, '#FF3E3E']]
                       )
        fig_heat.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#8B949E',
            font_family='JetBrains Mono',
            margin=dict(l=0, r=0, t=10, b=10),
            height=250,
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_heat, use_container_width=True, config={'displayModeBar': False})
        if walkthrough_mode:
            st.markdown("""
                <div style="font-size: 0.8rem; color: #8B949E; border-left: 2px solid #FF3E3E; padding: 10px; background-color: rgba(255, 62, 62, 0.05);">
                    <strong>ATTENTION:</strong> ASIA_PACIFIC jurisdiction shows significant drift (RED) in AML reasoning patterns.
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with right_col:
        # HUD Panel: Live Cognitive Stream
        st.markdown('<div class="hud-panel" style="height: 620px; overflow-y: hidden;"><div class="hud-panel-title">Live Cognitive Stream</div>', unsafe_allow_html=True)
        
        events = APIClient.get_event_stream()
        if not events:
            events = [
                {"timestamp": "14:22:01", "category": "AML", "action": "Large block detected: APAC-CLUSTER-9", "severity": "HIGH"},
                {"timestamp": "14:21:45", "category": "FRAUD", "action": "Emulator signature match blocked.", "severity": "CRITICAL"},
                {"timestamp": "14:20:12", "category": "GOV", "action": "Policy evolution recommended: KYC-V4", "severity": "INFO"},
                {"timestamp": "14:18:55", "category": "OPS", "action": "Node synchronization complete.", "severity": "INFO"},
                {"timestamp": "14:15:33", "category": "REG", "action": "SAR Filing auto-drafted: CASE-8821", "severity": "MEDIUM"}
            ]
        
        for e in events[:8]:
            sev = e.get('severity', 'INFO').upper()
            color = "#00FF41" if sev == "INFO" else "#FFD700" if sev in ["MEDIUM", "WARNING"] else "#FF3E3E"
            glow = "rgba(0, 255, 65, 0.1)" if sev == "INFO" else "rgba(255, 215, 0, 0.1)" if sev in ["MEDIUM", "WARNING"] else "rgba(255, 62, 62, 0.1)"
            
            st.markdown(f"""
                <div style="background-color: #080A0E; border-left: 2px solid {color}; padding: 12px; margin-bottom: 12px; border: 1px solid #1B1F24; box-shadow: inset 4px 0 10px {glow};">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                        <span style="font-size: 0.6rem; color: #8B949E; font-family: 'JetBrains Mono';">{e.get('timestamp', 'NOW')} UTC</span>
                        <span style="font-size: 0.6rem; color: {color}; font-weight: 700; font-family: 'JetBrains Mono';">[{sev}]</span>
                    </div>
                    <div style="font-size: 0.75rem; color: #F0F6FC; font-weight: 500; font-family: 'Inter';">{e.get('action', 'EVENT_EMITTED')}</div>
                    <div style="font-size: 0.6rem; color: #484F58; margin-top: 5px; font-family: 'JetBrains Mono';">DOMAIN: {e.get('category', 'SYS')}</div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- FOOTER ACTIONS ---
    st.markdown('<div class="hud-panel"><div class="hud-panel-title">Institutional Command & Control</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("TRIGGER DRILL: AML ESCALATION", use_container_width=True, type="primary"):
            st.warning("INITIATING AML ESCALATION DRILL...")
            from demo.orchestration.scenario_orchestrator import ScenarioOrchestrator
            from demo.scenarios.scenario_registry import get_aml_escalation_scenario
            import asyncio
            orch = ScenarioOrchestrator()
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(orch.execute_scenario(get_aml_escalation_scenario()))
            st.success("AML Drill Sequence Triggered.")
    with c2:
        if st.button("APPROVE GOVERNANCE EVOLUTION", use_container_width=True):
            st.success("Evolution Proposal Transmitted to Board.")
    with c3:
        if st.button("AUDIT REPLAY: APAC", use_container_width=True):
            st.info("Replay Initialized for APAC Jurisdiction.")
    with c4:
        if st.button("EMERGENCY PROTOCOL: ZERO_TRUST", use_container_width=True):
            st.error("Protocol Activated: Institutional Data Locking Initiated.")
    st.markdown('</div>', unsafe_allow_html=True)
