from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger("esoteric_platform.exceptions")

class PlatformException(Exception):
    def __init__(self, message: str, status_code: int = 500, error_code: str = "INTERNAL_ERROR"):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.message)

def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(PlatformException)
    async def platform_exception_handler(request: Request, exc: PlatformException):
        logger.error(f"PlatformException: {exc.message} (Code: {exc.error_code})")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "meta": {
                    "status": "error",
                    "code": exc.error_code,
                },
                "error": {
                    "message": exc.message,
                    "details": str(exc)
                }
            }
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled Exception: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "meta": {
                    "status": "error",
                    "code": "UNHANDLED_SYSTEM_ERROR",
                },
                "error": {
                    "message": "An unexpected enterprise platform error occurred."
                }
            }
        )