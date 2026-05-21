# ESOTERIC BANK Data Platform Stabilization

Institutional-grade data warehouse and ETL stabilization infrastructure for local deployment.

## Components

### 1. Database Runtime Validation (`database/scripts/runtime_validator.py`)
Ensures PostgreSQL connectivity, version compatibility, and institutional user permissions.

### 2. ETL Startup Validation (`etl/scripts/startup_validator.py`)
Verifies the presence of required institutional source data (CSV) and ensures necessary output directories exist.

### 3. Warehouse Health Checks (`warehouse/scripts/health_checks.py`)
Validates schema integrity by checking for critical institutional tables and verifying data presence.

### 4. Migration Execution (`database/scripts/migrate.py`)
Orchestrates the foundational SQL schema and transformation lifecycle.

### 5. Seed Orchestration (`etl/scripts/seed_orchestrator.py`)
Automates the generation of synthetic institutional data and triggers the initial ETL pipeline.

## Local Runtime Recommendations

- **PostgreSQL Version**: 15.x is recommended for institutional consistency.
- **Resources**: Allocate at least 2GB of RAM to the PostgreSQL process for optimal transformation performance.
- **Disk Space**: Ensure at least 5GB of free space for synthetic data generation and warehouse expansion.
- **Connection Pooling**: For local development, `psycopg2` direct connections are sufficient. For production, integrate `PgBouncer`.

## Operations Workflow

1. **Initialize Database**:
   ```bash
   python database/scripts/runtime_validator.py
   ```

2. **Execute Migrations**:
   ```bash
   python database/scripts/migrate.py
   ```

3. **Seed Data & Initial ETL**:
   ```bash
   python etl/scripts/seed_orchestrator.py
   ```

4. **Verify Health**:
   ```bash
   python warehouse/scripts/health_checks.py
   ```
