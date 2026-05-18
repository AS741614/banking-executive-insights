
-- =========================
-- PERFORMANCE INDEXES
-- =========================

CREATE INDEX IF NOT EXISTS ix_ft_date
ON mart.fact_transaction(date_key);

CREATE INDEX IF NOT EXISTS ix_ft_acct
ON mart.fact_transaction(account_sk);

CREATE INDEX IF NOT EXISTS ix_acct_cust
ON mart.dim_account(customer_sk);

-- =========================
-- EXECUTIVE ENRICHED VIEW
-- =========================

CREATE OR REPLACE VIEW mart.vw_transaction_enriched AS

SELECT
    ft.txn_id,
    dd.full_date,
    dd.year,
    dd.quarter,
    dd.month_name,

    c.segment,
    c.country,

    p.product_name,
    p.product_type,

    b.region,
    b.branch_name,

    ft.txn_type,
    ft.amount,
    ft.signed_amount

FROM mart.fact_transaction ft

JOIN mart.dim_date dd
    ON dd.date_key = ft.date_key

JOIN mart.dim_account a
    ON a.account_sk = ft.account_sk

JOIN mart.dim_customer c
    ON c.customer_sk = a.customer_sk

JOIN mart.dim_product p
    ON p.product_sk = a.product_sk

JOIN mart.dim_branch b
    ON b.branch_sk = a.branch_sk;

-- =========================
-- MATERIALIZED KPI VIEW
-- =========================

CREATE MATERIALIZED VIEW IF NOT EXISTS mart.mv_kpi_month AS

SELECT
    year,
    month_name,
    segment,
    product_type,
    region,

    COUNT(*) AS txn_count,
    SUM(amount) AS gross_amount,
    SUM(signed_amount) AS net_flow

FROM mart.vw_transaction_enriched

GROUP BY
    year,
    month_name,
    segment,
    product_type,
    region;

CREATE INDEX IF NOT EXISTS ix_mv_kpi_seg
ON mart.mv_kpi_month(segment, product_type);

