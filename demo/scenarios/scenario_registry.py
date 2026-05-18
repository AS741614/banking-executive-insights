from typing import List
from demo.models.scenario_models import DemoScenario, DemoStep, ScenarioCategory
from ai.events.models.event import EventCategory, EventSeverity

def get_aml_escalation_scenario() -> DemoScenario:
    """
    Returns the AML Escalation demo scenario.
    Demonstrates: Detection -> Analysis -> Escalation -> Executive Governance.
    """
    return DemoScenario(
        scenario_id="SCN-AML-001",
        name="Institutional AML Escalation",
        category=ScenarioCategory.AML,
        executive_narrative="A high-velocity transaction sequence is detected in a high-risk jurisdiction, triggering automated multi-agent reasoning and executive escalation.",
        steps=[
            DemoStep(
                step_id="STEP-1",
                order=1,
                title="Anomaly Detection",
                description="Cognitive engine detects unusual velocity pattern in Account #8821.",
                action_type="EMIT_EVENT",
                payload={
                    "severity": EventSeverity.MEDIUM,
                    "action": "ANOMALY_DETECTED",
                    "data": {"account": "8821", "pattern": "HIGH_VELOCITY"}
                },
                delay_sec=3
            ),
            DemoStep(
                step_id="STEP-2",
                order=2,
                title="Cross-Domain Analysis",
                description="AML Surveillance Engine correlates anomaly with high-risk jurisdiction exposure.",
                action_type="EMIT_EVENT",
                payload={
                    "severity": EventSeverity.HIGH,
                    "action": "AML_SURVEILLANCE_ANALYSIS",
                    "data": {"jurisdiction": "TIER_3", "aml_severity": 0.88}
                },
                delay_sec=4,
                governance_commentary="Automated correlation identified regulatory risk variance exceeding institutional thresholds."
            ),
            DemoStep(
                step_id="STEP-3",
                order=3,
                title="Executive Escalation",
                description="System triggers mandatory governance escalation for TIER_4 executive review.",
                action_type="GOVERNANCE_ESCALATION",
                payload={"data": {"case_id": "AML-2026-X", "priority": "URGENT"}},
                delay_sec=5
            ),
            DemoStep(
                step_id="STEP-4",
                order=4,
                title="SAR Recommendation",
                description="Cognitive orchestrator generates formal SAR recommendation narrative.",
                action_type="EMIT_EVENT",
                payload={
                    "severity": EventSeverity.CRITICAL,
                    "action": "SAR_RECOMMENDATION_GENERATED",
                    "data": {"narrative_preview": "Suspected layering via multi-hop cross-border transfers..."}
                },
                delay_sec=2
            )
        ]
    )

def get_fraud_prevention_scenario() -> DemoScenario:
    """
    Returns the Fraud Prevention demo scenario.
    Demonstrates: Device Intelligence -> ATO Detection -> Automated Blocking.
    """
    return DemoScenario(
        scenario_id="SCN-FRD-001",
        name="Real-time Fraud Prevention",
        category=ScenarioCategory.FRAUD,
        executive_narrative="Device intelligence identifies a high-risk emulator session combined with geographical drift, leading to an automated institutional block.",
        steps=[
            DemoStep(
                step_id="STEP-1",
                order=1,
                title="Device Profiling",
                description="Hardware layer detects emulator signature and VPN exposure.",
                action_type="EMIT_EVENT",
                payload={
                    "severity": EventSeverity.HIGH,
                    "action": "DEVICE_RISK_IDENTIFIED",
                    "data": {"emulator": True, "vpn": True}
                },
                delay_sec=3
            ),
            DemoStep(
                step_id="STEP-2",
                order=2,
                title="Behavioral Synthesis",
                description="Fraud engine identifies account takeover (ATO) pattern with 92% confidence.",
                action_type="EMIT_EVENT",
                payload={
                    "severity": EventSeverity.CRITICAL,
                    "action": "FRAUD_COGNITION_COMPLETE",
                    "data": {"ato_probability": 0.92, "action": "BLOCK"}
                },
                delay_sec=4
            )
        ]
    )
