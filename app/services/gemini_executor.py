import asyncio
import logging
from typing import Tuple
from app.core.config import settings
from app.core.exceptions import PlatformException

logger = logging.getLogger("esoteric_platform.services.gemini_executor")

class GeminiCLIExecutor:
    """
    Centralized execution utility for the Gemini CLI.
    Provides a cognitive execution abstraction layer.
    """
    
    @staticmethod
    async def execute_prompt(prompt: str, context_dir: str = None) -> Tuple[str, str]:
        """
        Executes a prompt using the Gemini CLI via subprocess.
        Returns (stdout, stderr).
        """
        cmd = [settings.GEMINI_CLI_PATH, "--prompt", prompt]
        if context_dir:
            cmd.extend(["--context", context_dir])
            
        logger.info(f"Executing Gemini CLI cognition: {' '.join(cmd)}")
        
        try:
            # We use asyncio.create_subprocess_exec for async non-blocking execution
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(), 
                    timeout=settings.COGNITION_TIMEOUT_SEC
                )
            except asyncio.TimeoutError:
                process.kill()
                logger.error("Gemini CLI execution timed out.")
                raise PlatformException(
                    message="Cognition execution timed out",
                    status_code=504,
                    error_code="COGNITION_TIMEOUT"
                )
            
            out_str = stdout.decode('utf-8').strip() if stdout else ""
            err_str = stderr.decode('utf-8').strip() if stderr else ""
            
            if process.returncode != 0:
                logger.warning(f"Gemini CLI returned non-zero code ({process.returncode}): {err_str}")
                # We might not strictly fail on non-zero if the CLI returns partial intelligence
                # but we should log it.
                
            return out_str, err_str
            
        except FileNotFoundError:
            logger.error(f"Gemini CLI binary not found at {settings.GEMINI_CLI_PATH}")
            raise PlatformException(
                message="Cognitive engine unavailable",
                status_code=503,
                error_code="ENGINE_UNAVAILABLE"
            )
        except Exception as e:
            logger.error(f"Unexpected error executing Gemini CLI: {e}")
            raise PlatformException(
                message="Failed to execute cognitive cycle",
                status_code=500,
                error_code="COGNITION_EXECUTION_ERROR"
            )