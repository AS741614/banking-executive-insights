import streamlit as st
import asyncio
from datetime import datetime
from ai.executive.copilot.engine import ExecutiveCopilotEngine, CopilotMessage
from ui.components.theme import render_institutional_header

# Singleton engine instance for the UI session
if 'copilot_engine' not in st.session_state:
    st.session_state.copilot_engine = ExecutiveCopilotEngine()

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [
        CopilotMessage(role="assistant", content="Institutional Copilot active. How may I assist your executive reasoning today?")
    ]

def render_copilot_console():
    """
    Renders the ESOTERIC Executive Copilot conversational interface.
    """
    render_institutional_header("AI Copilot Reasoning Console")
    
    st.markdown("""
        <div style="background-color: #0D1117; padding: 15px; border-radius: 4px; border-left: 5px solid #00FF41; border: 1px solid #1B1F24; margin-bottom: 20px;">
            <strong>Institutional Persona Active:</strong> Executive Advisor Mode (Tier 4 Clearance)
        </div>
    """, unsafe_allow_html=True)

    # Display Chat History
    for message in st.session_state.chat_history:
        with st.chat_message(message.role):
            st.markdown(message.content)
            st.caption(f"{message.timestamp.strftime('%H:%M:%S')} UTC")

    # Executive Input
    if prompt := st.chat_input("Query Institutional Brain..."):
        # Add user message to history
        user_msg = CopilotMessage(role="user", content=prompt)
        st.session_state.chat_history.append(user_msg)
        
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate Assistant Response
        with st.chat_message("assistant"):
            with st.spinner("Reasoning over institutional datasets..."):
                # Run the async engine
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                response = loop.run_until_complete(
                    st.session_state.copilot_engine.generate_response(prompt, st.session_state.chat_history)
                )
                
                st.markdown(response.content)
                st.caption(f"{response.timestamp.strftime('%H:%M:%S')} UTC")
                
                # Show reasoning context if available
                if "intent" in response.metadata:
                    with st.expander("View Cognitive Reasoning Context"):
                        st.json(response.metadata)
                
                st.session_state.chat_history.append(response)

    # Sidebar Tools for Copilot
    with st.sidebar:
        st.subheader("Copilot Cognitive Tools")
        if st.button("RESET COGNITIVE CONTEXT"):
            st.session_state.chat_history = [
                CopilotMessage(role="assistant", content="Institutional Copilot active. How may I assist your executive reasoning today?")
            ]
            st.rerun()
            
        st.markdown("---")
        st.subheader("Context Awareness")
        st.info("Currently observing: TIER_1_ASSETS, AML_RISK_POSTURE, LIQUIDITY_FLOWS")
        st.subheader("Copilot Intelligence Tiers")
        st.checkbox("Regulatory Intelligence", value=True)
        st.checkbox("Treasury Reasoning", value=True)
        st.checkbox("Fraud Cognition", value=True)
