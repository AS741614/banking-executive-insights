# ESOTERIC BANK Infrastructure & Enterprise Security

Institutional-grade infrastructure, deployment, and security architecture.

## Security Architecture

### 1. Authentication & JWT (`app/security/jwt.py`)
- Implementation of secure JWT token generation and validation.
- Password hashing using `bcrypt` via `passlib`.
- Configurable token expiration and secret key management.

### 2. RBAC Authorization (`app/security/rbac.py` & `app/api/deps/security.py`)
- Role-Based Access Control framework with pre-defined institutional roles:
  - `EXECUTIVE`
  - `COMPLIANCE_OFFICER`
  - `RISK_ANALYST`
  - `PLATFORM_ADMIN`
  - `SYSTEM_AGENT`
- `RoleChecker` dependency for FastAPI to enforce granular access control on endpoints.

## Infrastructure & Deployment

### 1. Docker Orchestration (`docker/Dockerfile.enterprise` & `docker-compose.enterprise.yml`)
- Multi-stage Docker build optimized for production.
- Separate targets for `api` (FastAPI) and `ui` (Streamlit).
- Health checks and network isolation for institutional resilience.

### 2. CI/CD Pipeline (`.github/workflows/enterprise_ci.yml`)
- Automated validation: Linting (Ruff), Security Scanning (Bandit), and Unit Testing (Pytest).
- Automated Docker build and registry pushing for the `main` branch.

## Operations

### Secrets Management
Secrets should be managed via environment variables or a dedicated secrets manager (e.g., AWS Secrets Manager, HashiCorp Vault).
- `SECRET_KEY`: Critical for JWT signing.
- `API_KEY`: For external service integrations.

### Deployment Topology
The platform is designed for containerized deployment (Kubernetes/ECS) with a clear separation between the cognitive API gateway and the executive visualization layer.
