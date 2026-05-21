import streamlit as st
import asyncio
from demo.orchestration.scenario_orchestrator import ScenarioOrchestrator
from demo.scenarios.scenario_registry import get_aml_escalation_scenario, get_fraud_prevention_scenario
from ui.components.theme import render_institutional_header

def render_demo_control_center():
    render_institutional_header("Institutional Demo Control Center")
    
    st.markdown("### Crisis Simulation & Executive Demonstration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Available Scenarios")
        
        scenario_choice = st.selectbox(
            "Select Scenario",
            [
                "Institutional AML Escalation", 
                "Real-time Fraud Prevention", 
                "Institutional Governance Escalation",
                "APAC Liquidity Deterioration"
            ]
        )
        
        from demo.scenarios.scenario_registry import (
            get_aml_escalation_scenario, 
            get_fraud_prevention_scenario,
            get_governance_escalation_scenario,
            get_liquidity_crisis_scenario
        )

        if scenario_choice == "Institutional AML Escalation":
            scenario = get_aml_escalation_scenario()
        elif scenario_choice == "Real-time Fraud Prevention":
            scenario = get_fraud_prevention_scenario()
        elif scenario_choice == "Institutional Governance Escalation":
            scenario = get_governance_escalation_scenario()
        elif scenario_choice == "APAC Liquidity Deterioration":
            scenario = get_liquidity_crisis_scenario()
        else:
            scenario = None
            
        if scenario:
            st.info(f"**Narrative:** {scenario.executive_narrative}")
            st.write(f"**Category:** {scenario.category}")
            st.write(f"**Steps:** {len(scenario.steps)}")
            
            if st.button("INITIATE SCENARIO", use_container_width=True, type="primary"):
                st.session_state.active_scenario = scenario
                st.session_state.scenario_running = True
                st.success(f"Scenario {scenario.name} initialized.")
    
    with col2:
        st.subheader("Crisis Injection (Manual)")
        st.warning("Manual crisis injection bypasses orchestrated narratives.")
        
        from testing.final_cascade.crisis_injector import InstitutionalCrisisInjector
        injector = InstitutionalCrisisInjector()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        if st.button("INJECT LIQUIDITY DETERIORATION", use_container_width=True):
            loop.run_until_complete(injector.inject_liquidity_deterioration())
            st.error("Liquidity Stress Signal Transmitted.")
            
        if st.button("INJECT COORDINATED FRAUD ATTACK", use_container_width=True):
            loop.run_until_complete(injector.inject_coordinated_fraud_attack())
            st.error("Fraud Attack Vector Injected.")
            
        if st.button("INJECT GOVERNANCE DRIFT", use_container_width=True):
            loop.run_until_complete(injector.inject_governance_drift())
            st.error("Governance Drift Event Emitted.")

    st.markdown("---")
    
    st.subheader("Institutional Replay Mode")
    if "event_logs" not in st.session_state:
        st.session_state.event_logs = []
        
    if not st.session_state.event_logs:
        st.info("No active event logs available for replay. Complete a scenario first.")
    else:
        st.success(f"Captured {len(st.session_state.event_logs)} institutional events.")
        speed = st.slider("Replay Speed Factor", 0.5, 5.0, 1.0)
        if st.button("START REPLAY", use_container_width=True):
            from demo.orchestration.replay_engine import InstitutionalReplayEngine
            engine = InstitutionalReplayEngine()
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            st.warning("REPLAY IN PROGRESS... Check dashboards for state evolution.")
            loop.run_until_complete(engine.replay_sequence(st.session_state.event_logs, speed_factor=speed))
            st.success("Replay sequence completed.")

    st.markdown("---")
    
    if st.session_state.get("scenario_running", False):
        st.subheader("Scenario Progress")
        progress_bar = st.progress(0)
        
        # Capture logs if scenario just finished
        if st.session_state.active_scenario:
            # Note: This is a bit of a hack for the demo
            # In a real app, the orchestrator would update a shared state
            from demo.orchestration.scenario_orchestrator import ScenarioOrchestrator
            orch = ScenarioOrchestrator()
            
            # Simulate execution for logging purposes if we are in this thread
            # This allows the UI to 'see' what happened
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(orch.execute_scenario(st.session_state.active_scenario))
            st.session_state.event_logs = orch.get_replay_data()
            st.session_state.scenario_running = False
            st.success("Scenario completed and logged.")
            st.rerun()

if __name__ == "__main__":
    # For testing isolation
    render_demo_control_center()
