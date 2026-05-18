import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from ui.components.theme import render_institutional_header

def render_aml_kyc_dashboard():
    render_institutional_header("Regulatory & Compliance Cockpit")
    
    tabs = st.tabs(["AML_SURVEILLANCE", "KYC_INTELLIGENCE", "FRAUD_PATTERNS"])
    
    with tabs[0]:
        st.markdown('<div class="hud-panel"><div class="hud-panel-title">Transaction Monitoring & Alert Matrix</div>', unsafe_allow_html=True)
        col1, col2 = st.columns([6, 4])
        
        with col1:
            regions = ["EMEA", "AMER", "APAC", "LATAM"]
            alert_types = ["Structuring", "Layering", "Sanctions", "Velocity"]
            z_data = np.random.randint(0, 50, size=(len(regions), len(alert_types)))
            
            fig = px.imshow(z_data, labels=dict(x="Alert Type", y="Region", color="Volume"),
                           x=alert_types, y=regions, 
                           color_continuous_scale=[[0, '#0D1117'], [0.5, '#FFD700'], [1, '#FF3E3E']])
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#8B949E',
                font_family='JetBrains Mono',
                margin=dict(l=0, r=0, t=20, b=0),
                height=350,
                coloraxis_showscale=False
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        with col2:
            st.markdown('<div style="font-size: 0.7rem; color: #8B949E; font-family: \'JetBrains Mono\'; margin-bottom: 10px;">MANDATORY_SAR_RECOMMENDATIONS</div>', unsafe_allow_html=True)
            for i in range(3):
                with st.expander(f"SAR-REC-2026-00{i+1}: HIGH_SEVERITY"):
                    st.write("**Entity:** Institutional Client #8821")
                    st.write("**Trigger:** Multi-hop cross-border layering.")
                    st.write("**Narrative:** Cognitive engines identified a structured sequence of 14 transfers across 3 jurisdictions in < 4ms.")
                    st.button(f"AUTHORIZE FILING: 00{i+1}", key=f"sar_{i}", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[1]:
        st.markdown('<div class="hud-panel"><div class="hud-panel-title">Customer Risk Concentration</div>', unsafe_allow_html=True)
        df = pd.DataFrame({
            "Client Segment": ["HNWI", "Institutional", "Retail", "Corporate", "FinTech"],
            "KYC Risk": [0.12, 0.08, 0.45, 0.22, 0.88],
            "AML Severity": [0.15, 0.10, 0.35, 0.25, 0.92],
            "Escalation Status": ["STABLE", "STABLE", "MONITOR", "STABLE", "URGENT"]
        })
        st.dataframe(df, hide_index=True, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[2]:
        st.markdown('<div class="hud-panel"><div class="hud-panel-title">Fraud Intelligence Pattern Discovery</div>', unsafe_allow_html=True)
        c1, c2 = st.columns([1, 1])
        with c1:
            st.json({
                "active_threat_vectors": ["Account Takeover", "Synthetic Identity", "Deepfake Auth"],
                "global_confidence_avg": 0.942,
                "blocked_volume_24h": "$4.2M",
                "detected_rings": 2
            })
        with c2:
            st.info("Threat Replay Engine ready for simulation.")
            if st.button("TRIGGER THREAT REPLAY", use_container_width=True):
                st.warning("Replay Initialized...")
        st.markdown('</div>', unsafe_allow_html=True)
