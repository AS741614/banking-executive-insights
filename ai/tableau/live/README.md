# ESOTERIC BANK Tableau Live Connectivity

Enterprise-grade analytics bridge between the institutional PostgreSQL warehouse and Tableau Desktop.

## Architecture
- **Framework**: Modular Python-based Connectivity Engine
- **Orchestration**: `sync_tableau.py` for runtime synchronization.
- **Validation**: `WarehouseConnectivityValidator` for automated connection probes and latency measurement.
- **Security**: Hardened institutional credential mapping via `TableauConnectionConfig`.

## Connectivity Workflow

1. **Hardened Configuration**: The platform uses Pydantic-based configuration to map warehouse parameters directly to Tableau-compatible settings.
2. **Connectivity Validation**: Before any analytical operations, the validator ensures the warehouse is accessible and all institutional views (e.g., `mv_kpi_month`) are present.
3. **Runtime Sync**: A dedicated script provides the necessary connection metadata for Tableau Desktop to establish a live link.

## Operational Execution

To synchronize the analytics bridge and verify institutional connectivity:

```bash
python ai/tableau/live/scripts/sync_tableau.py
```

## Performance Monitoring
The infrastructure includes specialized probes to measure analytical latency, ensuring that executive dashboards remain responsive even during high-volume cognitive cycles.

## Tableau Desktop Integration
- **Server**: `localhost` (default for local deployment)
- **Port**: `5432`
- **Database**: `esoteric_bank`
- **Username**: `esoteric_admin`
- **Authentication**: `Username and Password`
- **SSL**: `Required`
