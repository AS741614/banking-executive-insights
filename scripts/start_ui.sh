#!/bin/bash

# ESOTERIC Executive Command Center - Local Startup Script
# Stabilized for local deployment

echo "--- STARTING ESOTERIC EXECUTIVE COMMAND CENTER ---"

# 1. Run Pre-flight Checks
python3 ui/utils/runtime_validator.py
if [ $? -ne 0 ]; then
    echo "CRITICAL: Pre-flight checks failed. Aborting."
    exit 1
fi

# 2. Check for .env file
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        echo "WARNING: .env not found. Creating from .env.example"
        cp .env.example .env
    else
        echo "WARNING: .env and .env.example not found. Proceeding with defaults."
    fi
fi

# 3. Start Streamlit UI
echo "Launching Streamlit Gateway..."
export PYTHONPATH=$PYTHONPATH:.
streamlit run ui/main.py --server.port 8501 --server.address 0.0.0.0
