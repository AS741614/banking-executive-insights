import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from ui.components.theme import render_institutional_header

from ui.utils.api_client import APIClient

def render_treasury_dashboard():
    render_institutional_header("Institutional Treasury Cockpit")
    
    # --- DATA FETCHING ---
    exec_intel = APIClient.get_executive_intelligence()
    
    # --- TOP TIER LIQUIDITY METRICS ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        liquidity = exec_intel.get("net_liquidity", "$142.5B")
        st.metric("Net Liquidity", liquidity, "+1.2B")
    with col2:
        tier1 = exec_intel.get("tier_1_ratio", "14.8%")
        st.metric("Tier 1 Capital Ratio", tier1, "STABLE")
    with col3:
        hqla = exec_intel.get("hqla_level", "112%")
        st.metric("HQLA Level", hqla, "+2%")
    with col4:
        velocity = exec_intel.get("intraday_velocity", "0.82")
        st.metric("Intraday Velocity", velocity, "-0.05")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- MAIN TREASURY ANALYTICS ---
    left_col, right_col = st.columns([7, 3])
    
    with left_col:
        st.markdown('<div class="hud-panel"><div class="hud-panel-title">Global Liquidity Flows & Stress Projections</div>', unsafe_allow_html=True)
        
        # Projection Chart
        dates = pd.date_range(start='2026-05-18', periods=30, freq='D')
        
        proj_data = exec_intel.get("liquidity_projections")
        if proj_data:
            projections = pd.DataFrame(proj_data)
        else:
            projections = pd.DataFrame({
                'Date': dates,
                'Baseline': 100 + np.random.randn(30).cumsum(),
                'Stress_Scenario_A': 100 + np.random.randn(30).cumsum() - 2,
                'Stress_Scenario_B': 100 + np.random.randn(30).cumsum() - 5
            })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=projections.get('Date', projections.index), y=projections['Baseline'], name='BASELINE_LIQUIDITY', line=dict(color='#00FF41', width=3)))
        fig.add_trace(go.Scatter(x=projections.get('Date', projections.index), y=projections['Stress_Scenario_A'], name='STRESS_L1', line=dict(color='#FFD700', width=2, dash='dash')))
        fig.add_trace(go.Scatter(x=projections.get('Date', projections.index), y=projections['Stress_Scenario_B'], name='STRESS_L2_CRITICAL', line=dict(color='#FF3E3E', width=2, dash='dot')))
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#8B949E',
            font_family='JetBrains Mono',
            margin=dict(l=0, r=0, t=20, b=0),
            height=350,
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=True, gridcolor='#1B1F24', zeroline=False),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=10))
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="hud-panel"><div class="hud-panel-title">Counterparty Risk Matrix</div>', unsafe_allow_html=True)
        
        risk_matrix = exec_intel.get("counterparty_risk")
        if risk_matrix:
            df_risk = pd.DataFrame(risk_matrix)
        else:
            df_risk = pd.DataFrame({
                "Counterparty": ["CENTRAL_BANK_A", "INTERBANK_HUB_B", "RETAIL_SEGMENT_C", "TECH_PARTNER_D"],
                "Exposure": ["$42B", "$28B", "$12B", "$4.5B"],
                "Rating": ["AAA", "AA-", "BBB+", "A"],
                "Limit_Usage": ["45%", "62%", "88%", "22%"],
                "Trend": ["STABLE", "DEGRADING", "STABLE", "IMPROVING"]
            })
        st.table(df_risk)
        st.markdown('</div>', unsafe_allow_html=True)

    with right_col:
        st.markdown('<div class="hud-panel"><div class="hud-panel-title">Treasury Actions</div>', unsafe_allow_html=True)
        
        recommendation = exec_intel.get("treasury_recommendation", "Adaptive Liquidity Engine recommends re-balancing APAC hub due to projected outflow.")
        st.info(recommendation)
        
        if st.button("EXECUTE RE-BALANCING", use_container_width=True):
            st.success("Re-balancing order transmitted to Global Execution Desk.")
        
        if st.button("TRIGGER STRESS TEST: REPLAY_2008", use_container_width=True):
            st.warning("Stress Test Initialized. Computational load increasing.")
            
        st.markdown("---")
        st.subheader("Yield Optimization")
        st.metric("Portfolio Yield", exec_intel.get("portfolio_yield", "4.25%"), "+0.12%")
        st.metric("Alpha Generation", exec_intel.get("alpha_gen", "0.45%"), "+0.05%")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="hud-panel"><div class="hud-panel-title">Asset Allocation</div>', unsafe_allow_html=True)
        
        allocation = exec_intel.get("asset_allocation", {'CASH': 30, 'TREASURIES': 50, 'ABS': 15, 'OTHER': 5})
        
        # Simple donut chart
        fig_pie = go.Figure(data=[go.Pie(labels=list(allocation.keys()), 
                                       values=list(allocation.values()),
                                       hole=.6,
                                       marker=dict(colors=['#00FF41', '#FFD700', '#FF3E3E', '#8B949E']))])
        fig_pie.update_layout(
            showlegend=False,
            margin=dict(l=0, r=0, t=0, b=0),
            height=200,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
