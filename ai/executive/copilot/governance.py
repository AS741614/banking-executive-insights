import logging
from typing import Dict, Any
from ai.executive.copilot.engine import CopilotMessage

logger = logging.getLogger("ai.executive.copilot.governance")

class CopilotGovernanceLayer:
    """
    Ensures every conversational interaction follows institutional governance policies.
    """
    
    def __init__(self):
        self.restricted_terms = ["personal_data", "unencrypted_secrets", "bypass_policy"]

    def validate_interaction(self, query: str, response: CopilotMessage) -> bool:
        """
        Validates both the input query and the generated response for governance compliance.
        """
        # 1. Input Sanitization Check
        if any(term in query.lower() for term in self.restricted_terms):
            logger.warning(f"Governance Violation: Restricted term detected in query.")
            return False
            
        # 2. Output Leakage Check
        if any(term in response.content.lower() for term in self.restricted_terms):
            logger.error(f"Critical Governance Violation: Potential data leakage in assistant response.")
            return False
            
        # 3. Tone & Authority Check
        # Ensure the assistant is not making unauthorized commitments
        if "I promise" in response.content or "I guarantee" in response.content:
             logger.warning("Governance Warning: Assistant using unauthorized commitment language.")
             # We might allow it but log it
             
        return True

    def mask_sensitive_data(self, content: str) -> str:
        """
        Masks any potential sensitive identifiers in the conversational stream.
        """
        # Simple placeholder for more complex regex-based masking
        return content.replace("INTERNAL_SECRET_001", "[REDACTED_BY_GOVERNANCE]")
