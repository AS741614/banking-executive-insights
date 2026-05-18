import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field

logger = logging.getLogger("ai.executive.copilot.engine")

class CopilotMessage(BaseModel):
    role: str # 'user', 'assistant', 'system'
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)

from ai.executive.copilot.prompts import INSTITUTIONAL_PERSONA
from ai.executive.briefings.engine import BriefingEngine
from ai.executive.strategy.reasoning import StrategicReasoningLayer

class ExecutiveCopilotEngine:
    """
    Core conversational reasoning engine for the ESOTERIC Executive Copilot.
    Handles KPI interpretation, governance Q&A, and operational recommendations.
    """
    
    def __init__(self, state_registry=None):
        from ai.executive.copilot.governance import CopilotGovernanceLayer
        self.state = state_registry
        self.persona = INSTITUTIONAL_PERSONA
        self.governance = CopilotGovernanceLayer()
        self.briefing_engine = BriefingEngine()
        self.strategic_reasoner = StrategicReasoningLayer()

    async def generate_response(self, query: str, chat_history: List[CopilotMessage]) -> CopilotMessage:
        """
        Generates a reasoned response based on the executive query and institutional state.
        """
        logger.info(f"Processing executive query: {query}")
        
        # 1. Intent Classification (Simulated)
        intent = self._classify_intent(query)
        
        # 2. Institutional Knowledge Retrieval (Simulated)
        context = self._retrieve_institutional_context(intent)
        
        # 3. Reasoning & Response Generation
        response_content = self._reason_and_formulate(query, intent, context)
        
        response = CopilotMessage(
            role="assistant",
            content=response_content,
            metadata={"intent": intent, "context_used": list(context.keys())}
        )

        # 4. Governance Validation
        if not self.governance.validate_interaction(query, response):
            response.content = "I apologize, but I cannot fulfill this request as it violates institutional governance policies."
            response.metadata["governance_rejection"] = True

        return response

    def _classify_intent(self, query: str) -> str:
        query_l = query.lower()
        if any(w in query_l for w in ["kpi", "performance", "volume", "flow"]):
            return "KPI_EXPLANATION"
        if any(w in query_l for w in ["risk", "aml", "fraud", "compliance"]):
            return "RISK_GOVERNANCE"
        if any(w in query_l for w in ["recommend", "action", "suggest", "improve"]):
            return "STRATEGIC_RECOMMENDATION"
        return "GENERAL_INQUIRY"

    def _retrieve_institutional_context(self, intent: str) -> Dict[str, Any]:
        """
        Retrieves data from specialized intelligence engines based on intent.
        """
        context = {}
        if intent == "KPI_EXPLANATION":
            briefing = self.briefing_engine.generate_daily_briefing()
            context["kpi_data"] = briefing.key_metrics
            context["institutional_summary"] = briefing.summary
        elif intent == "RISK_GOVERNANCE":
            briefing = self.briefing_engine.generate_daily_briefing()
            context["risk_posture"] = {
                "alerts": briefing.critical_alerts,
                "governance_commentary": briefing.governance_commentary
            }
        elif intent == "STRATEGIC_RECOMMENDATION":
            reasoning = self.strategic_reasoner.reason_over_liquidity_drift("APAC", 0.28)
            context["strategic_reasoning"] = reasoning
            
        return context

    def _reason_and_formulate(self, query: str, intent: str, context: Dict[str, Any]) -> str:
        """
        Formulates a reasoned, explainable response with high operational realism.
        """
        if intent == "KPI_EXPLANATION":
            metrics = context['kpi_data']
            return (
                f"Executive Performance Brief: Institutional AUM is currently {metrics['AUM']} with a "
                f"Liquidity Coverage Ratio of {metrics['Liquidity_Coverage_Ratio']}. "
                f"Summary: {context['institutional_summary']}\n\n"
                "I recommend focusing on the regional dispersion of these flows, particularly in the APAC segment."
            )
        elif intent == "RISK_GOVERNANCE":
            risk = context['risk_posture']
            alerts_str = "\n".join([f"- {a}" for a in risk['alerts']])
            return (
                f"Governance & Risk Posture:\n{risk['governance_commentary']}\n\n"
                f"Active Critical Signals:\n{alerts_str}\n\n"
                "Does this alignment with the 2026 Framework meet your requirements for the board briefing?"
            )
        elif intent == "STRATEGIC_RECOMMENDATION":
            strat = context['strategic_reasoning']
            return (
                f"Strategic Recommendation for {strat['region']} (Priority: {strat['urgency']}):\n"
                f"Rationale: {strat['rationale']}\n"
                f"Proposed Action: {strat['recommendation']}\n\n"
                "This action is designed to stabilize regional drift and ensure institutional continuity."
            )
        else:
            return (
                "Institutional Copilot active. I am ready to provide reasoning over "
                "KPI performance, risk governance, or strategic recommendations. "
                "How may I assist your executive reasoning today?"
            )
