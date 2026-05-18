import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from ui.components.theme import render_institutional_header

def render_aml_kyc_dashboard():
    render_institutional_header("Regulatory & Compliance Cockpit")
    
    tabs = st.tabs(["AML Surveillance", "KYC Intelligence", "Fraud Pattern Analysis"])
    
    with tabs[0]:
        st.subheader("Transaction Monitoring & Alert Matrix")
        col1, col2 = st.columns([6, 4])
        
        with col1:
            # Heatmap of alert volume by region and type
            regions = ["EMEA", "AMER", "APAC", "LATAM"]
            alert_types = ["Structuring", "Layering", "Sanctions", "Velocity"]
            z_data = np.random.randint(0, 50, size=(len(regions), len(alert_types)))
            
            fig = px.imshow(z_data, labels=dict(x="Alert Type", y="Region", color="Volume"),
                           x=alert_types, y=regions, color_continuous_scale='Greens')
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#8B949E',
                margin=dict(l=0, r=0, t=20, b=0),
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("### Mandatory SAR Recommendations")
            for i in range(3):
                with st.expander(f"SAR-REC-2026-00{i+1}: High Severity"):
                    st.write("**Entity:** Institutional Client #8821")
                    st.write("**Trigger:** Multi-hop cross-border layering.")
                    st.write("**Narrative Preview:** Cognitive engines identified a structured sequence of 14 transfers...")
                    st.button(f"AUTHORIZE FILING: 00{i+1}", key=f"sar_{i}")

    with tabs[1]:
        st.subheader("Customer Risk Heatmaps")
        st.info("Mapping institutional risk concentration across global segments.")
        # Dataframe with custom coloring would be nice here
        df = pd.DataFrame({
            "Client Segment": ["HNWI", "Institutional", "Retail", "Corporate", "FinTech"],
            "KYC Risk": [0.12, 0.08, 0.45, 0.22, 0.88],
            "AML Severity": [0.15, 0.10, 0.35, 0.25, 0.92],
            "Escalation Status": ["STABLE", "STABLE", "MONITOR", "STABLE", "URGENT"]
        })
        st.dataframe(df.style.background_gradient(cmap='RdYlGn_r', subset=['KYC Risk', 'AML Severity']), use_container_width=True)

    with tabs[2]:
        st.subheader("Fraud Intelligence Pattern Discovery")
        st.json({
            "active_threat_vectors": ["Account Takeover", "Synthetic Identity"],
            "global_confidence_avg": 0.942,
            "blocked_volume_24h": "$4.2M",
            "detected_rings": 2
        })
        st.button("TRIGGER THREAT REPLAY ENGINE")
