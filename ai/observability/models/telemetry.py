from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, ConfigDict

class CognitionTrace(BaseModel):
    trace_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_ms: Optional[float] = None
    steps: List[Dict[str, Any]] = Field(default_factory=list)
    status: str = "IN_PROGRESS"

class DriftReport(BaseModel):
    metric_name: str
    baseline_value: float
    current_value: float
    variance: float
    is_anomaly: bool = False
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class GovernanceTelemetry(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    
    telemetry_id: str
    component_id: str
    system_health: float = Field(..., ge=0.0, le=1.0)
    risk_exposure: float = Field(..., ge=0.0, le=1.0)
    drift_reports: List[DriftReport] = Field(default_factory=list)
    active_incidents: int = 0
    timestamp: datetime = Field(default_factory=datetime.utcnow)
