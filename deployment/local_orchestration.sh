#!/bin/bash
set -e

echo "--- ESOTERIC Platform: Local Enterprise Orchestration ---"

# 1. Validation
echo "[1/4] Validating institutional runtime..."
python scripts/validate_runtime.py

# 2. Build and Start
echo "[2/4] Initializing Docker orchestration topology..."
docker-compose -f docker-compose.enterprise.yml build
docker-compose -f docker-compose.enterprise.yml up -d

# 3. Wait for Health
echo "[3/4] Awaiting institutional service health..."
sleep 10
docker ps --filter "name=esoteric"

# 4. Summary
echo "[4/4] Orchestration complete."
echo "--------------------------------------------------"
echo "Executive Command Center : http://localhost:8501"
echo "Platform API Gateway     : http://localhost:8000"
echo "Observability (Grafana)  : http://localhost:3000"
echo "Observability (Prom)     : http://localhost:9090"
echo "--------------------------------------------------"
