from datetime import datetime
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class ScenarioCategory(str, Enum):
    AML = "AML"
    FRAUD = "FRAUD"
    GOVERNANCE = "GOVERNANCE"
    TREASURY = "TREASURY"
    OPERATIONAL = "OPERATIONAL"

class DemoStep(BaseModel):
    step_id: str
    order: int
    title: str
    description: str
    action_type: str  # EMIT_EVENT, INVOKE_API, UPDATE_UI
    payload: Dict[str, Any]
    delay_sec: int = 5
    governance_commentary: Optional[str] = None

class DemoScenario(BaseModel):
    scenario_id: str
    name: str
    category: ScenarioCategory
    executive_narrative: str
    steps: List[DemoStep]
    metadata: Dict[str, Any] = Field(default_factory=dict)
