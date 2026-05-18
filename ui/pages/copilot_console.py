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
    
    # --- EXECUTIVE STATUS BAR ---
    st.markdown("""
        <div style="display: flex; gap: 10px; margin-bottom: 20px;">
            <div class="hud-panel" style="flex: 1; padding: 10px; margin-bottom: 0;">
                <div style="font-size: 0.6rem; color: #8B949E; font-family: 'JetBrains Mono';">PERSONA_ACTIVE</div>
                <div style="font-size: 0.9rem; font-weight: 700; color: #00FF41;">EXECUTIVE_ADVISOR_V4</div>
            </div>
            <div class="hud-panel" style="flex: 1; padding: 10px; margin-bottom: 0;">
                <div style="font-size: 0.6rem; color: #8B949E; font-family: 'JetBrains Mono';">CLEARANCE_LEVEL</div>
                <div style="font-size: 0.9rem; font-weight: 700; color: #FFD700;">TIER_4_BOARD_DIRECT</div>
            </div>
            <div class="hud-panel" style="flex: 1; padding: 10px; margin-bottom: 0;">
                <div style="font-size: 0.6rem; color: #8B949E; font-family: 'JetBrains Mono';">COGNITION_SYNC</div>
                <div style="font-size: 0.9rem; font-weight: 700; color: #00FF41;">99.9% ACTIVE</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # --- CHAT INTERFACE ---
    chat_container = st.container(height=500, border=False)
    
    with chat_container:
        for message in st.session_state.chat_history:
            role_label = "COGNITIVE_CORE" if message.role == "assistant" else "EXECUTIVE_OPERATOR"
            role_color = "#00FF41" if message.role == "assistant" else "#8B949E"
            
            st.markdown(f"""
                <div style="margin-bottom: 20px;">
                    <div style="font-size: 0.6rem; color: {role_color}; font-family: 'JetBrains Mono'; margin-bottom: 5px;">
                        [{role_label}] // {message.timestamp.strftime('%H:%M:%S')} UTC
                    </div>
                    <div style="background-color: #0D1117; border: 1px solid #1B1F24; padding: 15px; border-radius: 2px; font-family: 'Inter'; font-size: 0.9rem; line-height: 1.5;">
                        {message.content}
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # Executive Input
    if prompt := st.chat_input("Query Institutional Brain..."):
        # Add user message to history
        user_msg = CopilotMessage(role="user", content=prompt)
        st.session_state.chat_history.append(user_msg)
        st.rerun()

    # Handling response generation (if last message is from user)
    if st.session_state.chat_history[-1].role == "user":
        with st.chat_message("assistant"):
            with st.spinner("Reasoning over institutional datasets..."):
                # Run the async engine
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                response = loop.run_until_complete(
                    st.session_state.copilot_engine.generate_response(st.session_state.chat_history[-1].content, st.session_state.chat_history[:-1])
                )
                
                st.session_state.chat_history.append(response)
                st.rerun()

    # Sidebar Tools for Copilot
    with st.sidebar:
        st.markdown('<div class="hud-panel"><div class="hud-panel-title">Copilot Configuration</div>', unsafe_allow_html=True)
        
        narration_mode = st.toggle("CRISIS NARRATION", value=False)
        if narration_mode:
            st.info("Narrating institutional signals...")
            
        if st.button("RESET CONTEXT", use_container_width=True):
            st.session_state.chat_history = [
                CopilotMessage(role="assistant", content="Institutional Copilot active. How may I assist your executive reasoning today?")
            ]
            st.rerun()
            
        st.markdown("---")
        st.subheader("Intelligence Tiers")
        st.checkbox("Regulatory Intelligence", value=True)
        st.checkbox("Treasury Reasoning", value=True)
        st.checkbox("Fraud Cognition", value=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- AUTO-NARRATION LOGIC ---
    if narration_mode:
        from ui.utils.api_client import APIClient
        events = APIClient.get_event_stream()
        if events:
            last_event = events[0]
            last_event_id = last_event.get("event_id")
            if st.session_state.get("last_narrated_event") != last_event_id:
                st.session_state.last_narrated_event = last_event_id
                
                narration = f"**INSTITUTIONAL SIGNAL DETECTED:** {last_event.get('action')}\n\n**Reasoning:** {last_event.get('payload', {}).get('narrative_preview', 'Automated analysis in progress...')}"
                st.session_state.chat_history.append(CopilotMessage(role="assistant", content=narration))
                st.rerun()
