#!/bin/bash

# ESOTERIC Executive Command Center - Secure Local Startup
# Stabilized for enterprise execution

echo "--- INITIALIZING ESOTERIC SECURE RUNTIME ---"

# 1. Environment Check
if [ ! -f .env ]; then
    echo "ERROR: .env file not found. Please create it from .env.example"
    exit 1
fi

# 2. Run Enterprise Configuration Validator
echo "Validating security configurations..."
python3 infra/config/validator.py
if [ $? -ne 0 ]; then
    echo "CRITICAL: Security validation failed. Aborting startup."
    exit 1
fi

# 3. Apply Secure Defaults
export PYTHONASYNCIODEBUG=0
export PYTHONHASHSEED=random

# 4. Start Services (Example: FastAPI Backend)
echo "Launching Secure API Gateway..."
# uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4 --limit-concurrency 100 --timeout-keep-alive 5
echo "Services ready. Monitor logs for cognitive events."
