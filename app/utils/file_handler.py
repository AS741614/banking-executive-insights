import os
import json
import logging
from typing import Any, Dict

logger = logging.getLogger("esoteric_platform.utils.file_handler")

def safe_read_json(filepath: str) -> Dict[str, Any]:
    if not os.path.exists(filepath):
        logger.warning(f"File not found: {filepath}")
        return {}
    
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from {filepath}: {e}")
        return {}
    except Exception as e:
        logger.error(f"Unexpected error reading {filepath}: {e}")
        return {}

def safe_write_json(filepath: str, data: Dict[str, Any]) -> bool:
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        logger.error(f"Error writing to {filepath}: {e}")
        return False