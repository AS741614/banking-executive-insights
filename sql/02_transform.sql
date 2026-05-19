
TRUNCATE mart.fact_transaction,
         mart.fact_account_month,
         mart.dim_account,
         mart.dim_customer,
         mart.dim_product,
         mart.dim_branch,
         mart.dim_date
RESTART IDENTITY CASCADE;

-- =========================
-- DATE DIMENSION
-- =========================

INSERT INTO mart.dim_date
SELECT
    to_char(d, 'YYYYMMDD')::INT,
    d::DATE,
    extract(year FROM d),
    extract(quarter FROM d),
    extract(month FROM d),
    to_char(d, 'Mon'),
    extract(day FROM d),
    (
        d = (
            date_trunc('month', d)
            + interval '1 month - 1 day'
        )
    )
FROM generate_series(
    '2023-01-01'::date,
    '2026-12-31'::date,
    '1 day'
) d;

-- =========================
-- DIMENSIONS
-- =========================

INSERT INTO mart.dim_customer (
    customer_id,
    full_name,
    segment,
    country,
    onboarded_date
)
SELECT
    customer_id,
    full_name,
    segment,
    country,
    onboarded_date
FROM staging.customers;

INSERT INTO mart.dim_product (
    product_id,
    product_name,
    product_type
)
SELECT
    product_id,
    product_name,
    product_type
FROM staging.products;

INSERT INTO mart.dim_branch (
    branch_id,
    branch_name,
    city,
    region
)
SELECT
    branch_id,
    branch_name,
    city,
    region
FROM staging.branches;

INSERT INTO mart.dim_account (
    account_id,
    customer_sk,
    product_sk,
    branch_sk,
    open_date,
    status
)
SELECT
    a.account_id,
    c.customer_sk,
    p.product_sk,
    b.branch_sk,
    a.open_date,
    a.status
FROM staging.accounts a
JOIN mart.dim_customer c
    ON c.customer_id = a.customer_id
JOIN mart.dim_product p
    ON p.product_id = a.product_id
JOIN mart.dim_branch b
    ON b.branch_id = a.branch_id;

-- =========================
-- FACT TRANSACTIONS
-- =========================

INSERT INTO mart.fact_transaction (
    txn_id,
    date_key,
    account_sk,
    txn_type,
    amount,
    signed_amount
)
SELECT
    t.txn_id,
    to_char(t.txn_date, 'YYYYMMDD')::INT,
    da.account_sk,
    t.txn_type,
    t.amount,
    CASE
        WHEN t.txn_type IN ('WITHDRAWAL', 'FEE')
            THEN -t.amount
        ELSE t.amount
    END
FROM staging.transactions t
JOIN mart.dim_account da
    ON da.account_id = t.account_id;

-- =========================
-- MONTHLY SNAPSHOT FACT
-- =========================

INSERT INTO mart.fact_account_month (
    account_sk,
    date_key,
    net_flow,
    txn_count
)
SELECT
    ft.account_sk,
    (dd.year * 10000 + dd.month * 100 + 1) AS date_key,
    SUM(ft.signed_amount),
    COUNT(*)
FROM mart.fact_transaction ft
JOIN mart.dim_date dd
    ON dd.date_key = ft.date_key
GROUP BY
    ft.account_sk,
    dd.year,
    dd.month;

