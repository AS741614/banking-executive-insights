#!/bin/bash

# ESOTERIC BANK | Executive Command Center - Startup Script
# Optimized for local deployment

# Colors for institutional feedback
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}>>> Initializing ESOTERIC BANK Intelligence Gateway...${NC}"

# 1. Validate Runtime
python3 ui/validate_runtime.py

# 2. Check if API is already running in background
curl -s http://localhost:8000/health > /dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}>>> Warning: Backend API (FastAPI) not detected at localhost:8000${NC}"
    echo -e "${YELLOW}>>> UI will be initialized in OFFLINE/MOCK mode.${NC}"
fi

# 3. Launch Streamlit
echo -e "${GREEN}>>> Launching Command Center Dashboard...${NC}"
export PYTHONPATH=$PYTHONPATH:.
streamlit run ui/main.py --server.port 8501 --server.address 0.0.0.0
