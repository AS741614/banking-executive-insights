import logging
import uuid
from datetime import datetime
from typing import List, Dict, Any

from ai.tableau.semantic.models.bi_models import (
    DashboardSpecification, 
    DashboardWidgetSpec, 
    KPIMetadata,
    KPISemanticCategory
)
from ai.tableau.cognition.engines.viz_recommendation import VisualizationRecommendationEngine

logger = logging.getLogger("esoteric_bank.tableau.cognition_service")

class DashboardCognitionService:
    """
    Enterprise Dashboard Cognition Service.
    Orchestrates the generation of governance-aware BI specifications.
    """

    def __init__(self):
        self.viz_engine = VisualizationRecommendationEngine()

    async def generate_dashboard_spec(
        self, 
        persona: str, 
        kpi_list: List[KPIMetadata]
    ) -> DashboardSpecification:
        """
        Generates a machine-readable dashboard specification based on executive persona.
        """
        logger.info(f"Generating dashboard cognition for persona: {persona}")
        
        widgets = []
        for i, kpi in enumerate(kpi_list):
            viz_type = self.viz_engine.recommend_visualization(kpi)
            
            widget = DashboardWidgetSpec(
                widget_id=f"WID-{uuid.uuid4().hex[:6].upper()}",
                title=f"{kpi.name} Analysis",
                viz_type=viz_type,
                kpi_references=[kpi.name],
                layout_position={"x": 0, "y": 0, "w": 6, "h": 4} # Placeholder, will be updated by engine
            )
            widgets.append(widget)

        # Apply layout intelligence
        widget_dicts = [w.model_dump() for w in widgets]
        positioned_widgets = self.viz_engine.recommend_layout(widget_dicts)
        
        final_widgets = [DashboardWidgetSpec(**pw) for pw in positioned_widgets]

        spec = DashboardSpecification(
            spec_id=f"SPEC-{uuid.uuid4().hex[:8].upper()}",
            title=f"Institutional Overview: {persona.replace('_', ' ')}",
            target_persona=persona,
            widgets=final_widgets,
            created_at=datetime.utcnow().isoformat(),
            last_cognitive_review=datetime.utcnow().isoformat()
        )

        logger.info(f"Dashboard specification generated: {spec.spec_id}")
        return spec

    def get_institutional_kpi_registry(self) -> List[KPIMetadata]:
        """Returns the core institutional KPI definitions."""
        return [
            KPIMetadata(
                name="AML_SEVERITY_INDEX",
                semantic_category=KPISemanticCategory.REGULATORY_COMPLIANCE,
                unit="Score (0-1)",
                description="Aggregated AML risk severity across all jurisdictions."
            ),
            KPIMetadata(
                name="TIER_1_LIQUIDITY_RATIO",
                semantic_category=KPISemanticCategory.LIQUIDITY,
                unit="Ratio",
                description="Core institutional liquidity metric."
            ),
            KPIMetadata(
                name="GOVERNANCE_DRIFT_SCORE",
                semantic_category=KPISemanticCategory.GOVERNANCE_DRIFT,
                unit="Variance",
                description="Measured deviation from institutional policy baselines."
            )
        ]
