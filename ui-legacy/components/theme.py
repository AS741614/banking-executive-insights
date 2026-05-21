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
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700&family=Inter:wght@300;400;600;700&family=Space+Grotesk:wght@300;400;700&display=swap');
        
        :root {
            --bloomberg-green: #00FF41;
            --bloomberg-yellow: #FFD700;
            --bloomberg-red: #FF3E3E;
            --bg-deep: #05070A;
            --bg-card: #0D1117;
            --border-institutional: #1B1F24;
            --border-bright: #30363D;
            --text-primary: #F0F6FC;
            --text-secondary: #8B949E;
            --accent-glow: rgba(0, 255, 65, 0.15);
        }

        /* Base Styles */
        .stApp {
            background-color: var(--bg-deep);
            color: var(--text-primary);
            font-family: 'Inter', sans-serif;
        }

        /* Scanline Effect */
        .stApp::before {
            content: " ";
            display: block;
            position: absolute;
            top: 0;
            left: 0;
            bottom: 0;
            right: 0;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.1) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.02), rgba(0, 255, 0, 0.01), rgba(0, 0, 255, 0.02));
            z-index: 100;
            background-size: 100% 2px, 3px 100%;
            pointer-events: none;
            opacity: 0.3;
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: var(--bg-deep);
        }
        ::-webkit-scrollbar-thumb {
            background: var(--border-institutional);
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: var(--text-secondary);
        }

        /* Sidebar Refinement */
        section[data-testid="stSidebar"] {
            background-color: #080A0E;
            border-right: 1px solid var(--border-institutional);
        }

        /* Institutional Metric Cards */
        div[data-testid="metric-container"] {
            background-color: var(--bg-card);
            border: 1px solid var(--border-institutional);
            padding: 24px;
            border-radius: 2px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.6);
            transition: border 0.3s ease;
        }
        
        div[data-testid="metric-container"]:hover {
            border: 1px solid var(--bloomberg-green);
        }

        div[data-testid="stMetricLabel"] {
            color: var(--text-secondary) !important;
            font-size: 0.65rem !important;
            text-transform: uppercase;
            letter-spacing: 0.2em;
            font-weight: 700;
            margin-bottom: 8px;
        }

        div[data-testid="stMetricValue"] {
            color: var(--bloomberg-green) !important;
            font-family: 'JetBrains Mono', monospace;
            font-size: 2.4rem !important;
            font-weight: 700;
            text-shadow: 0 0 10px var(--accent-glow);
        }

        /* Custom Header Components */
        .terminal-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            border-bottom: 1px solid var(--border-institutional);
            padding: 20px 0;
            margin-bottom: 40px;
            position: relative;
        }
        
        .terminal-header::after {
            content: "";
            position: absolute;
            bottom: -1px;
            left: 0;
            width: 150px;
            height: 2px;
            background-color: var(--bloomberg-green);
            box-shadow: 0 0 10px var(--bloomberg-green);
        }

        .terminal-brand {
            font-family: 'JetBrains Mono', monospace;
            color: var(--text-secondary);
            font-size: 0.7rem;
            font-weight: 400;
            letter-spacing: 2px;
            margin-bottom: 10px;
        }
        
        .terminal-title {
            font-family: 'Space Grotesk', sans-serif;
            margin:0; 
            padding:0; 
            font-size: 3rem; 
            font-weight: 700;
            letter-spacing: -2px;
            color: var(--text-primary);
        }

        .status-pill-live {
            background-color: rgba(0, 255, 65, 0.05);
            color: var(--bloomberg-green);
            border: 1px solid var(--bloomberg-green);
            padding: 4px 12px;
            border-radius: 2px;
            font-size: 0.6rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { opacity: 0.4; }
            50% { opacity: 1; }
            100% { opacity: 0.4; }
        }

        /* HUD Panels */
        .hud-panel {
            background-color: var(--bg-card);
            border: 1px solid var(--border-institutional);
            border-radius: 2px;
            padding: 20px;
            margin-bottom: 20px;
        }
        
        .hud-panel-title {
            color: var(--text-secondary);
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.15em;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
        }
        
        .hud-panel-title::before {
            content: "";
            display: inline-block;
            width: 4px;
            height: 12px;
            background-color: var(--bloomberg-green);
            margin-right: 10px;
        }

        /* High-density Dataframes */
        .stDataFrame {
            border: 1px solid var(--border-institutional);
        }
        
        /* Expander Styling */
        .st-emotion-cache-1h9up9z {
            background-color: var(--bg-card);
            border: 1px solid var(--border-institutional);
            border-radius: 2px;
        }

        /* Buttons */
        .stButton>button {
            background-color: transparent;
            color: var(--text-primary);
            border: 1px solid var(--border-institutional);
            border-radius: 2px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            border-color: var(--bloomberg-green);
            color: var(--bloomberg-green);
            box-shadow: 0 0 10px rgba(0, 255, 65, 0.2);
        }
        </style>
    """, unsafe_allow_html=True)

def render_institutional_header(title: str):
    now = datetime.utcnow().strftime("%Y-%m-%d // %H:%M:%S")
    st.markdown(f"""
        <div class="terminal-header">
            <div>
                <div class="terminal-brand">SYSTEM_OPERATIONAL // {now} UTC</div>
                <h1 class="terminal-title">{title}</h1>
            </div>
            <div style="text-align: right; padding-bottom: 5px;">
                <span class="status-pill-live">COGNITION_LINK_ACTIVE</span>
                <div style="color: var(--text-secondary); font-size: 0.7rem; margin-top: 10px; font-family: 'JetBrains Mono', monospace;">
                    AUTH: SEC_CLEARANCE_T4
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

