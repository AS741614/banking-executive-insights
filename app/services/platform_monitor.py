import time
import os
import psutil
from typing import Dict, Any

class PlatformMonitor:
    start_time = time.time()
    
    @staticmethod
    def get_health_status() -> Dict[str, Any]:
        uptime_seconds = time.time() - PlatformMonitor.start_time
        
        return {
            "status": "healthy",
            "uptime_seconds": uptime_seconds,
            "version": "1.0.0",
            "environment": os.getenv("ENVIRONMENT", "development")
        }
        
    @staticmethod
    def get_observability_metrics() -> Dict[str, Any]:
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        
        return {
            "cpu_percent": psutil.cpu_percent(),
            "memory_usage_mb": memory_info.rss / 1024 / 1024,
            "active_threads": process.num_threads(),
            "open_files": len(process.open_files())
        }