# ESOTERIC BANK Runtime Validation & Smoke Testing

Enterprise-grade operational readiness and smoke testing infrastructure for the ESOTERIC Platform.

## Architecture
- **Framework**: Modular Python-based Validation Suite
- **Orchestration**: `SmokeTestRunner` for full-lifecycle operational readiness checks.
- **Validators**: Specialized units for Dependencies, API Health, and Governance Engines.
- **Traceability**: Full institutional logging and status reporting for audit compliance.

## Core Validators

### 1. Dependency Validator (`runtime/validators/dependency_validator.py`)
Ensures all institutional environment variables (`SECRET_KEY`, `ENVIRONMENT`) and required platform directories are present.

### 2. API Validator (`runtime/validators/api_validator.py`)
Executes liveness and readiness probes against the FastAPI gateway, including deep validation of the cognition pipeline.

### 3. Governance Validator (`runtime/validators/governance_validator.py`)
Verifies that all regulatory (KYC, AML) and fraud cognition engines are correctly initialized and their governance logic is active.

## Operational Workflow

### Running a Smoke Test
Ensure the FastAPI server is running (`uvicorn app.main:app`), then execute the smoke test runner:

```bash
python -m runtime.smoke_test_runner
```

### Readiness Reporting
The system generates institutional-grade status outputs, classifying the platform as either `PASS` or `FAIL` based on critical safety and operational thresholds.

## Integration
The runtime validation domain is designed to integrate with CI/CD pipelines (GitHub Actions) and container orchestration health checks to ensure zero-downtime governance-safe deployments.
