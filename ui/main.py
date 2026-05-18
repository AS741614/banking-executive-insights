import streamlit as st
import requests
from ui.components.theme import apply_enterprise_theme, render_institutional_header

# Constants
API_URL = "http://localhost:8000/api/v1"

def main():
    apply_enterprise_theme()
    
    # Sidebar Navigation - Institutional Style
    st.sidebar.image("https://img.icons8.com/ios-filled/100/00FF41/bank-building.png", width=60)
    st.sidebar.markdown("<h1 style='text-align: center; color: #00FF41;'>ESOTERIC BANK</h1>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    
    selection = st.sidebar.radio(
        "COMMAND DOMAINS",
        [
            "EXECUTIVE_OVERVIEW",
            "REGULATORY_COCKPIT",
            "GOVERNANCE_COCKPIT",
            "AI_COPILOT_CONSOLE",
            "PLATFORM_OBSERVABILITY"
        ]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info(f"**Operator:** AKASH SHARMA\n\n**Clearance:** TIER_4_BOARD")
    st.sidebar.markdown("<div style='font-size: 0.7rem; color: #8B949E; text-align: center;'>INSTITUTIONAL_RESILIENCE_V1.0</div>", unsafe_allow_html=True)
    
    if selection == "EXECUTIVE_OVERVIEW":
        from ui.pages.executive_overview import render_executive_dashboard
        render_executive_dashboard()
    elif selection == "REGULATORY_COCKPIT":
        from ui.pages.compliance_center import render_aml_kyc_dashboard
        render_aml_kyc_dashboard()
    elif selection == "GOVERNANCE_COCKPIT":
        from ui.pages.governance_cockpit import render_governance_cockpit
        render_governance_cockpit()
    elif selection == "AI_COPILOT_CONSOLE":
        from ui.pages.copilot_console import render_copilot_console
        render_copilot_console()
    elif selection == "PLATFORM_OBSERVABILITY":
        from ui.main import render_observability_page # For now keep here
        render_observability_page()

def render_observability_page():
    render_institutional_header("Platform Observability")
    
    st.subheader("System Health & Infrastructure Topology")
    cols = st.columns(3)
    cols[0].metric("API Gateway", "ONLINE", "0.2ms")
    cols[1].metric("Cognitive Core", "HEALTHY", "1.4B Ops")
    cols[2].metric("Event Bus", "ACTIVE", "142 msg/s")

    st.markdown("---")
    st.subheader("Resource Utilization & Cognitive Load")
    st.progress(0.42, text="Memory Utilization: 42.5GB / 128GB")
    st.progress(0.15, text="GPU Cognition Clusters: 15.2%")
    
    st.subheader("Institutional Audit Logs")
    st.code("""
    [2026-05-18 14:22:01] TRACE-8821: AML Inference Complete.
    [2026-05-18 14:21:45] TRACE-9912: Fraud Anomaly Detected.
    [2026-05-18 14:20:12] SYSTEM: Policy Evolution Re-loaded.
    """)

if __name__ == "__main__":
    main()
