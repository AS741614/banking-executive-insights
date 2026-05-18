import logging
from app.schemas.intelligence import IntelligenceQuery, IntelligenceResponse
from app.services.gemini_executor import GeminiCLIExecutor

logger = logging.getLogger("esoteric_platform.services.cognition")

class CognitionService:
    @staticmethod
    async def generate_banking_intelligence(query: IntelligenceQuery) -> IntelligenceResponse:
        """
        Generates governance-aware banking cognition by dynamically invoking the Gemini CLI.
        """
        logger.info(f"Generating banking intelligence for prompt: {query.prompt[:50]}...")
        
        # In a real enterprise system, we'd inject context based on the governance level.
        # For now, we delegate directly to the Gemini executor.
        
        # Prepare the enhanced prompt with governance context
        enhanced_prompt = f"[Governance Level: {query.governance_level}] {query.prompt}"
        
        stdout, stderr = await GeminiCLIExecutor.execute_prompt(enhanced_prompt)
        
        # If output is empty but there's an error, that's an issue
        if not stdout and stderr:
            logger.error(f"Cognitive generation failed: {stderr}")
            return IntelligenceResponse(
                query=query.prompt,
                intelligence_payload="Cognitive generation failed due to an internal error.",
                confidence_score=0.0,
                sources=[]
            )
            
        # Parse or wrap the output
        return IntelligenceResponse(
            query=query.prompt,
            intelligence_payload=stdout or "No intelligence generated.",
            confidence_score=0.95 if stdout else 0.0,
            sources=["Gemini CLI Cognition Engine"]
        )