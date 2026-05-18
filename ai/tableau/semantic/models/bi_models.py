from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

class VisualizationType(str, Enum):
    TIME_SERIES = "TIME_SERIES"
    KPI_CARD = "KPI_CARD"
    HEATMAP = "HEATMAP"
    ALERT_STREAM = "ALERT_STREAM"
    TREEMAP = "TREEMAP"
    SANKEY = "SANKEY"

class KPISemanticCategory(str, Enum):
    LIQUIDITY = "LIQUIDITY"
    REGULATORY_COMPLIANCE = "REGULATORY_COMPLIANCE"
    FRAUD_PREVENTION = "FRAUD_PREVENTION"
    GOVERNANCE_DRIFT = "GOVERNANCE_DRIFT"
    INSTITUTIONAL_GROWTH = "INSTITUTIONAL_GROWTH"

class KPIMetadata(BaseModel):
    name: str
    semantic_category: KPISemanticCategory
    unit: str
    governance_threshold_high: Optional[float] = None
    governance_threshold_low: Optional[float] = None
    description: str

class DashboardWidgetSpec(BaseModel):
    widget_id: str
    title: str
    viz_type: VisualizationType
    kpi_references: List[str]
    layout_position: Dict[str, int] # e.g., {"x": 0, "y": 0, "w": 6, "h": 4}
    governance_clearance: str = "TIER_1"

class DashboardSpecification(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    
    spec_id: str
    title: str
    target_persona: str # e.g., "CHIEF_RISK_OFFICER"
    widgets: List[DashboardWidgetSpec]
    version: str = "1.0.0"
    created_at: str
    last_cognitive_review: Optional[str] = None
