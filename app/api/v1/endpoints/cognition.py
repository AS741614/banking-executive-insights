from fastapi import APIRouter, Depends, Request
from datetime import datetime
from typing import Any

from app.schemas.intelligence import IntelligenceQuery, IntelligenceResponse
from app.schemas.common import EnterpriseResponse, EnterpriseMetadata
from app.services.cognition_service import CognitionService

router = APIRouter()

@router.post("/query", response_model=EnterpriseResponse[IntelligenceResponse])
async def cognition_query(query: IntelligenceQuery, request: Request) -> Any:
    """
    Executes a dynamic cognitive query using the Gemini CLI.
    Generates institutional intelligence responses.
    """
    trace_id = request.headers.get("X-Enterprise-Trace-Id")
    
    # Generate intelligence
    intelligence_result = await CognitionService.generate_banking_intelligence(query)
    
    return EnterpriseResponse(
        meta=EnterpriseMetadata(
            status="success",
            timestamp=datetime.utcnow().isoformat(),
            trace_id=trace_id,
            version="1.0"
        ),
        data=intelligence_result
    )