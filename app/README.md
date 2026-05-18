# ESOTERIC BANK Intelligence Platform - API

Production-grade FastAPI application providing an enterprise intelligence platform gateway.

## Features
- Modular Routing Architecture
- Enterprise Observability Middleware
- Centralized Exception Handling
- Cognitive Abstraction Layer (Gemini CLI Integration)
- Standardized Enterprise JSON Responses

## Bootstrap Instructions

1. **Install Dependencies**
   Ensure your Python virtual environment is active and install FastAPI and its standard server (Uvicorn) along with other dependencies:
   ```bash
   pip install fastapi uvicorn pydantic pydantic-settings psutil
   ```

2. **Validate Runtime**
   Before starting the application, run the institutional runtime validation script to ensure all enterprise dependencies are present:
   ```bash
   python scripts/validate_runtime.py
   ```

3. **Run the Application**
   From the project root directory, run the FastAPI application using `uvicorn`:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

4. **Health and Readiness Probes**
   The platform provides standardized observability probes for enterprise deployment:
   - Liveness Probe: `http://localhost:8000/health`
   - Readiness Probe: `http://localhost:8000/ready`
   - Detailed Status: `http://localhost:8000/api/v1/platform/status`

5. **Access the API Documentation**
   Open your browser and navigate to:
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

4. **Environment Variables**
   You can configure the platform via environment variables:
   - `ENVIRONMENT`: (default: "development")
   - `DEBUG`: (default: "True")
   - `GEMINI_CLI_PATH`: Path to the Gemini CLI binary (default: "gemini")
   - `COGNITION_TIMEOUT_SEC`: Timeout for cognitive queries (default: "60")