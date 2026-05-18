-- ============================================================================
-- ESOTERIC BANK TABLEAU GOVERNANCE SCHEMA
-- ============================================================================

CREATE SCHEMA IF NOT EXISTS governance;

-- 1. DASHBOARD REGISTRY & HEALTH
CREATE TABLE IF NOT EXISTS governance.dashboard_inventory (
    dashboard_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dashboard_name TEXT NOT NULL,
    project_path TEXT,
    owner_email TEXT,
    is_executive BOOLEAN DEFAULT FALSE,
    criticality_tier INT DEFAULT 4, -- Tier 1 (Highest) to Tier 4
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_validated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS governance.dashboard_health_logs (
    log_id SERIAL PRIMARY KEY,
    dashboard_id UUID REFERENCES governance.dashboard_inventory(dashboard_id),
    status TEXT, -- 'HEALTHY', 'DEGRADED', 'UNAVAILABLE'
    latency_ms INT,
    error_message TEXT,
    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. DATASOURCE OBSERVABILITY
CREATE TABLE IF NOT EXISTS governance.datasource_metrics (
    datasource_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    datasource_name TEXT NOT NULL,
    source_type TEXT, -- 'POSTGRES', 'SNOWFLAKE', 'HYPER'
    schema_name TEXT,
    table_name TEXT,
    freshness_threshold_min INT DEFAULT 60,
    last_refreshed_at TIMESTAMP,
    row_count_baseline BIGINT,
    drift_status TEXT DEFAULT 'STABLE'
);

-- 3. KPI DRIFT REGISTRY
CREATE TABLE IF NOT EXISTS governance.kpi_drift_log (
    drift_id SERIAL PRIMARY KEY,
    kpi_name TEXT NOT NULL,
    dimension_scope TEXT, -- e.g., 'Region=APAC'
    baseline_value NUMERIC,
    current_value NUMERIC,
    drift_percentage NUMERIC,
    is_anomaly BOOLEAN DEFAULT FALSE,
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. STALE DASHBOARD TRACKER
CREATE TABLE IF NOT EXISTS governance.dashboard_usage (
    dashboard_id UUID REFERENCES governance.dashboard_inventory(dashboard_id),
    user_id TEXT,
    accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
