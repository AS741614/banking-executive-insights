import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from ui.components.theme import render_institutional_header

def render_treasury_dashboard():
    render_institutional_header("Institutional Treasury Cockpit")
    
    # --- TOP TIER LIQUIDITY METRICS ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Net Liquidity", "$142.5B", "+1.2B")
    with col2:
        st.metric("Tier 1 Capital Ratio", "14.8%", "STABLE")
    with col3:
        st.metric("HQLA Level", "112%", "+2%")
    with col4:
        st.metric("Intraday Velocity", "0.82", "-0.05")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- MAIN TREASURY ANALYTICS ---
    left_col, right_col = st.columns([7, 3])
    
    with left_col:
        st.markdown('<div class="hud-panel"><div class="hud-panel-title">Global Liquidity Flows & Stress Projections</div>', unsafe_allow_html=True)
        
        # Projection Chart
        dates = pd.date_range(start='2026-05-18', periods=30, freq='D')
        projections = pd.DataFrame({
            'Date': dates,
            'Baseline': 100 + np.random.randn(30).cumsum(),
            'Stress_Scenario_A': 100 + np.random.randn(30).cumsum() - 2,
            'Stress_Scenario_B': 100 + np.random.randn(30).cumsum() - 5
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=projections['Date'], y=projections['Baseline'], name='BASELINE_LIQUIDITY', line=dict(color='#00FF41', width=3)))
        fig.add_trace(go.Scatter(x=projections['Date'], y=projections['Stress_Scenario_A'], name='STRESS_L1', line=dict(color='#FFD700', width=2, dash='dash')))
        fig.add_trace(go.Scatter(x=projections['Date'], y=projections['Stress_Scenario_B'], name='STRESS_L2_CRITICAL', line=dict(color='#FF3E3E', width=2, dash='dot')))
        
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
        st.info("Adaptive Liquidity Engine recommends re-balancing APAC hub due to projected outflow.")
        
        if st.button("EXECUTE RE-BALANCING", use_container_width=True):
            st.success("Re-balancing order transmitted to Global Execution Desk.")
        
        if st.button("TRIGGER STRESS TEST: REPLAY_2008", use_container_width=True):
            st.warning("Stress Test Initialized. Computational load increasing.")
            
        st.markdown("---")
        st.subheader("Yield Optimization")
        st.metric("Portfolio Yield", "4.25%", "+0.12%")
        st.metric("Alpha Generation", "0.45%", "+0.05%")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="hud-panel"><div class="hud-panel-title">Asset Allocation</div>', unsafe_allow_html=True)
        # Simple donut chart
        fig_pie = go.Figure(data=[go.Pie(labels=['CASH', 'TREASURIES', 'ABS', 'OTHER'], 
                                       values=[30, 50, 15, 5],
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
