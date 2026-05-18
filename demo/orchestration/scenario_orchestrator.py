import asyncio
import logging
import uuid
from datetime import datetime
from typing import List, Dict, Any

from demo.models.scenario_models import DemoScenario, DemoStep
from ai.events.engines.event_bus import event_bus
from ai.events.models.event import CognitiveEvent, EventCategory, EventSeverity

logger = logging.getLogger("esoteric_bank.demo.orchestrator")

class ScenarioOrchestrator:
    """
    Enterprise Scenario Orchestrator.
    Manages the execution of institutional intelligence demo workflows.
    """

    def __init__(self):
        self.active_scenario: Optional[DemoScenario] = None
        self.current_step_index: int = 0

    async def execute_scenario(self, scenario: DemoScenario):
        """
        Executes a full demo scenario step-by-step.
        """
        self.active_scenario = scenario
        logger.info(f"--- STARTING DEMO SCENARIO: {scenario.name} ---")
        logger.info(f"Narrative: {scenario.executive_narrative}")

        for step in sorted(scenario.steps, key=lambda x: x.order):
            await self._execute_step(step)
            logger.info(f"Step {step.order} complete. Waiting {step.delay_sec}s for next sequence...")
            await asyncio.sleep(step.delay_sec)

        logger.info(f"--- DEMO SCENARIO COMPLETE: {scenario.name} ---")

    async def _execute_step(self, step: DemoStep):
        """
        Executes a single institutional demo step.
        """
        logger.info(f"[STEP {step.order}] {step.title}: {step.description}")
        
        if step.action_type == "EMIT_EVENT":
            await self._emit_cognitive_event(step)
        elif step.action_type == "GOVERNANCE_ESCALATION":
            await self._emit_governance_escalation(step)
        
        if step.governance_commentary:
            logger.info(f"Governance Insights: {step.governance_commentary}")

    async def _emit_cognitive_event(self, step: DemoStep):
        payload = step.payload
        event = CognitiveEvent(
            event_id=f"DEMO-{uuid.uuid4().hex[:8].upper()}",
            trace_id=f"TRACE-DEMO-{self.active_scenario.scenario_id}",
            category=payload.get("category", EventCategory.OPERATIONAL),
            severity=payload.get("severity", EventSeverity.INFO),
            source_component="DemoOrchestrator",
            action=payload.get("action", "DEMO_EVENT"),
            payload=payload.get("data", {}),
            governance_context={"demo_step": step.step_id}
        )
        await event_bus.publish(event)

    async def _emit_governance_escalation(self, step: DemoStep):
        payload = step.payload
        event = CognitiveEvent(
            event_id=f"DEMO-ESC-{uuid.uuid4().hex[:8].upper()}",
            trace_id=f"TRACE-DEMO-{self.active_scenario.scenario_id}",
            category=EventCategory.GOVERNANCE,
            severity=EventSeverity.HIGH,
            source_component="DemoOrchestrator",
            action="GOVERNANCE_ESCALATION_TRIGGERED",
            payload=payload.get("data", {}),
            governance_context={
                "escalation_reason": step.description,
                "demo_mode": True
            }
        )
        await event_bus.publish(event)

from typing import Optional
