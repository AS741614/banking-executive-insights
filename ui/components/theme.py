import streamlit as st
from datetime import datetime

def apply_enterprise_theme():
    """
    Applies the ESOTERIC Institutional Aesthetic: Ultra-Dark High-Density Terminal.
    Optimized for executive command center immersion.
    """
    st.set_page_config(
        page_title="ESOTERIC BANK // Executive Command Center",
        page_icon="🏛️",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700&family=Inter:wght@300;400;600;700&display=swap');
        
        :root {
            --bloomberg-green: #00FF41;
            --bloomberg-yellow: #FFD700;
            --bloomberg-red: #FF3E3E;
            --bg-deep: #05070A;
            --bg-card: #0D1117;
            --border-institutional: #1B1F24;
            --text-primary: #F0F6FC;
            --text-secondary: #8B949E;
        }

        .stApp {
            background-color: var(--bg-deep);
            color: var(--text-primary);
            font-family: 'Inter', sans-serif;
        }

        /* Sidebar Refinement */
        section[data-testid="stSidebar"] {
            background-color: #0A0D12;
            border-right: 1px solid var(--border-institutional);
        }

        /* Institutional Metric Cards */
        div[data-testid="metric-container"] {
            background-color: var(--bg-card);
            border: 1px solid var(--border-institutional);
            padding: 20px;
            border-radius: 4px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.5);
        }

        div[data-testid="stMetricLabel"] {
            color: var(--text-secondary) !important;
            font-size: 0.75rem !important;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            font-weight: 600;
        }

        div[data-testid="stMetricValue"] {
            color: var(--bloomberg-green) !important;
            font-family: 'JetBrains Mono', monospace;
            font-size: 2.2rem !important;
            font-weight: 700;
        }

        /* Custom Header Components */
        .terminal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid var(--bloomberg-green);
            padding: 10px 0;
            margin-bottom: 30px;
        }

        .terminal-brand {
            font-family: 'JetBrains Mono', monospace;
            color: var(--bloomberg-green);
            font-weight: 700;
            letter-spacing: 4px;
        }

        .status-pill-live {
            background-color: rgba(0, 255, 65, 0.1);
            color: var(--bloomberg-green);
            border: 1px solid var(--bloomberg-green);
            padding: 2px 10px;
            border-radius: 12px;
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { opacity: 0.6; }
            50% { opacity: 1; }
            100% { opacity: 0.6; }
        }

        /* High-density Dataframes */
        .stDataFrame {
            border: 1px solid var(--border-institutional);
        }
        
        /* Expander Styling */
        .st-emotion-cache-1h9up9z {
            background-color: var(--bg-card);
            border: 1px solid var(--border-institutional);
        }
        </style>
    """, unsafe_allow_html=True)

def render_institutional_header(title: str):
    now = datetime.utcnow().strftime("%H:%M:%S")
    st.markdown(f"""
        <div class="terminal-header">
            <div>
                <div class="terminal-brand">ESOTERIC_BANK_SYSTEM // {now} UTC</div>
                <h1 style="margin:0; padding:0; font-size: 2.5rem; letter-spacing: -1px;">{title}</h1>
            </div>
            <div style="text-align: right;">
                <span class="status-pill-live">COGNITION_LINK_ACTIVE</span>
                <div style="color: var(--text-secondary); font-size: 0.8rem; margin-top: 5px;">
                    Operator: SEC_CLEARANCE_TIER_4
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
