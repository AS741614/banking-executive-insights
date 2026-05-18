import json
import logging
from datetime import datetime
from typing import Any, Dict

class InstitutionalJSONFormatter(logging.Formatter):
    """
    Structured JSON Formatter for Institutional Observability.
    Optimized for machine-readable cognitive and governance logs.
    """
    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "trace_id": getattr(record, "trace_id", "GLOBAL"),
            "category": getattr(record, "category", "OPERATIONAL")
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_record)

def setup_structured_logging():
    logger = logging.getLogger("esoteric_bank.observability")
    handler = logging.StreamHandler()
    handler.setFormatter(InstitutionalJSONFormatter())
    logger.addHandler(handler)
    logger.propagate = False
    return logger

structured_logger = setup_structured_logging()
