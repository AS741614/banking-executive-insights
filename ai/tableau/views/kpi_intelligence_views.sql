-- ============================================================================
-- ESOTERIC BANK INTELLIGENCE PLATFORM
-- TABLEAU KPI INTELLIGENCE VIEWS
-- ============================================================================

CREATE SCHEMA IF NOT EXISTS intelligence;

-- 1. EXECUTIVE KPI VIEW: Institutional Health & Performance
-- Optimized for Tableau high-level dashboards
CREATE OR REPLACE VIEW intelligence.vw_executive_kpis AS
WITH monthly_metrics AS (
    SELECT
        dd.year,
        dd.month,
        dd.month_name,
        c.segment,
        b.region,
        SUM(ft.amount) as total_volume,
        SUM(ft.signed_amount) as net_capital_flow,
        COUNT(DISTINCT a.account_id) as active_accounts,
        COUNT(ft.txn_id) as transaction_velocity
    FROM mart.fact_transaction ft
    JOIN mart.dim_date dd ON ft.date_key = dd.date_key
    JOIN mart.dim_account a ON ft.account_sk = a.account_sk
    JOIN mart.dim_customer c ON a.customer_sk = c.customer_sk
    JOIN mart.dim_branch b ON a.branch_sk = b.branch_sk
    GROUP BY 1, 2, 3, 4, 5
)
SELECT 
    *,
    AVG(net_capital_flow) OVER (PARTITION BY segment, region ORDER BY year, month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) as rolling_3m_flow
FROM monthly_metrics;

-- 2. AML INTELLIGENCE VIEW: Regulatory Compliance & Risk
-- Focuses on high-velocity and cross-border risk indicators
CREATE OR REPLACE VIEW intelligence.vw_aml_intelligence AS
SELECT
    ft.txn_id,
    dd.full_date,
    c.customer_id,
    c.full_name,
    c.country,
    c.segment,
    p.product_type,
    ft.amount,
    ft.txn_type,
    CASE 
        WHEN ft.amount > 10000 THEN 'HIGH_VALUE'
        WHEN ft.amount > 50000 THEN 'CRITICAL'
        ELSE 'STANDARD'
    END as aml_tier,
    -- Simple layering indicator: count of transactions > 5000 in same day per account
    COUNT(*) OVER (PARTITION BY a.account_sk, dd.date_key) as daily_frequency
FROM mart.fact_transaction ft
JOIN mart.dim_date dd ON ft.date_key = dd.date_key
JOIN mart.dim_account a ON ft.account_sk = a.account_sk
JOIN mart.dim_customer c ON a.customer_sk = c.customer_sk
JOIN mart.dim_product p ON a.product_sk = p.product_sk
WHERE ft.amount > 5000;

-- 3. FRAUD INTELLIGENCE VIEW: Pattern Recognition & Attack Vectors
-- Identifies potential account takeovers or Structuring
CREATE OR REPLACE VIEW intelligence.vw_fraud_intelligence AS
WITH daily_agg AS (
    SELECT
        a.account_id,
        a.account_sk,
        b.region,
        dd.full_date,
        SUM(ft.amount) as daily_burn_rate,
        COUNT(ft.txn_id) as daily_velocity,
        AVG(ft.amount) as avg_ticket_size
    FROM mart.fact_transaction ft
    JOIN mart.dim_date dd ON ft.date_key = dd.date_key
    JOIN mart.dim_account a ON ft.account_sk = a.account_sk
    JOIN mart.dim_branch b ON a.branch_sk = b.branch_sk
    GROUP BY 1, 2, 3, 4
)
SELECT
    *,
    STDDEV(daily_burn_rate) OVER (PARTITION BY account_sk ORDER BY full_date ROWS BETWEEN 30 PRECEDING AND CURRENT ROW) as volatility_index
FROM daily_agg;

-- 4. GOVERNANCE KPI AGGREGATIONS: Drift & Policy Adherence
CREATE OR REPLACE VIEW intelligence.vw_governance_metrics AS
SELECT
    b.region,
    p.product_type,
    c.segment,
    COUNT(DISTINCT c.customer_id) as total_customers,
    COUNT(CASE WHEN a.status = 'ACTIVE' THEN 1 END)::FLOAT / COUNT(*)::FLOAT as account_health_ratio,
    SUM(CASE WHEN ft.amount > 100000 THEN 1 ELSE 0 END) as institutional_exposures
FROM mart.dim_customer c
JOIN mart.dim_account a ON c.customer_sk = a.customer_sk
JOIN mart.dim_product p ON a.product_sk = p.product_sk
JOIN mart.dim_branch b ON a.branch_sk = b.branch_sk
LEFT JOIN mart.fact_transaction ft ON a.account_sk = ft.account_sk
GROUP BY 1, 2, 3;

-- 5. OBSERVABILITY INTELLIGENCE VIEW: Platform Performance
-- Mapped for monitoring the intelligence pipeline
CREATE OR REPLACE VIEW intelligence.vw_observability_kpis AS
SELECT
    dd.year,
    dd.month_name,
    COUNT(ft.txn_id) as processed_events,
    SUM(ft.amount) / 1000000.0 as processed_volume_millions,
    (COUNT(DISTINCT ft.account_sk)::FLOAT / COUNT(DISTINCT a.account_sk)::FLOAT) * 100 as account_activity_index
FROM mart.fact_transaction ft
CROSS JOIN (SELECT COUNT(*) as total_accts FROM mart.dim_account) a_total
JOIN mart.dim_account a ON ft.account_sk = a.account_sk
JOIN mart.dim_date dd ON ft.date_key = dd.date_key
GROUP BY 1, 2;

-- 6. ADAPTIVE KPI AGGREGATION: Intelligence Materialization
-- High-density view for Tableau extract performance
DROP MATERIALIZED VIEW IF EXISTS intelligence.mv_adaptive_intelligence_summary;
CREATE MATERIALIZED VIEW intelligence.mv_adaptive_intelligence_summary AS
SELECT
    year,
    month_name,
    region,
    segment,
    SUM(total_volume) as total_vol,
    SUM(transaction_velocity) as total_vel,
    AVG(active_accounts) as avg_active_accounts
FROM intelligence.vw_executive_kpis
GROUP BY 1, 2, 3, 4;

CREATE INDEX IF NOT EXISTS ix_ais_region_segment ON intelligence.mv_adaptive_intelligence_summary(region, segment);
