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
            "TREASURY_COCKPIT",
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
    elif selection == "TREASURY_COCKPIT":
        from ui.pages.treasury_cockpit import render_treasury_dashboard
        render_treasury_dashboard()
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
        from ui.pages.observability_panel import render_observability_page
        render_observability_page()

if __name__ == "__main__":
    main()
