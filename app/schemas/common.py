from pydantic import BaseModel, Field
from typing import Any, Dict, Optional, Generic, TypeVar

T = TypeVar('T')

class EnterpriseMetadata(BaseModel):
    status: str = Field(..., description="Status of the response (e.g., success, error)")
    timestamp: str = Field(..., description="ISO 8601 timestamp")
    trace_id: Optional[str] = Field(None, description="Enterprise tracking trace ID")
    latency_ms: Optional[float] = Field(None, description="Processing latency in milliseconds")
    version: str = Field("1.0", description="API Version")

class EnterpriseResponse(BaseModel, Generic[T]):
    meta: EnterpriseMetadata
    data: Optional[T] = None
    error: Optional[Dict[str, Any]] = None