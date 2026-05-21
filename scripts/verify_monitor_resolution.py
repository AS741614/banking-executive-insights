import os
import asyncio
from runtime.health.monitor import ServiceHealthMonitor

async def test_resolution(mode, env, db_url=None):
    os.environ["RUNTIME_MODE"] = mode
    os.environ["ENVIRONMENT"] = env
    if db_url:
        os.environ["DATABASE_URL"] = db_url
    else:
        os.environ.pop("DATABASE_URL", None)
        
    print(f"\nTesting Mode: {mode} | Env: {env} | DB_URL: {db_url}")
    
    # We need to simulate the init logic of monitor_institutional_stack
    # Since it's a while loop, I'll just check the initial resolution part
    
    env_val = os.getenv("ENVIRONMENT", "development")
    runtime_mode = os.getenv("RUNTIME_MODE", "auto")
    
    db_url_val = os.getenv("DATABASE_URL")
    db_host = os.getenv("DB_HOST")
    db_port = 5432

    if not db_host:
        if runtime_mode == "docker":
            db_host = "db"
        elif runtime_mode == "local":
            db_host = "localhost"
        else:
            db_host = "db" if env_val == "production" else "localhost"

    if db_url_val:
        from urllib.parse import urlparse
        try:
            parsed = urlparse(db_url_val)
            if parsed.hostname:
                db_host = parsed.hostname
            if parsed.port:
                db_port = parsed.port
        except Exception:
            pass

    print(f"Resolved DB: {db_host}:{db_port}")
    
    intentional_degraded = not db_url_val or runtime_mode == "frontend-only"
    print(f"Intentional Degraded: {intentional_degraded}")

if __name__ == "__main__":
    asyncio.run(test_resolution("docker", "production"))
    asyncio.run(test_resolution("local", "development"))
    asyncio.run(test_resolution("auto", "production"))
    asyncio.run(test_resolution("frontend-only", "production"))
    asyncio.run(test_resolution("hybrid", "production", "postgresql://user:pass@remote:5432/db"))
