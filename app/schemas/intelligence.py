from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class IntelligenceQuery(BaseModel):
    prompt: str = Field(..., description="The executive prompt for banking intelligence")
    context: Optional[Dict[str, Any]] = Field(None, description="Optional banking context")
    governance_level: Optional[str] = Field("STANDARD", description="Data governance level (e.g., STRICT, STANDARD)")

class IntelligenceResponse(BaseModel):
    query: str
    intelligence_payload: str
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    sources: Optional[List[str]] = None
    
class CognitiveAgentTask(BaseModel):
    agent_id: str
    task_description: str
    parameters: Optional[Dict[str, Any]] = None

class CognitiveAgentResult(BaseModel):
    agent_id: str
    status: str
    result: str
    execution_time_ms: float