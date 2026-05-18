
SELECT
    'txn_rowcount_recon' AS check_name,
    (SELECT COUNT(*) FROM staging.transactions) AS expected,
    (SELECT COUNT(*) FROM mart.fact_transaction) AS actual

UNION ALL

SELECT
    'txn_amount_recon',
    (
        SELECT ROUND(SUM(amount), 0)
        FROM staging.transactions
    ),
    (
        SELECT ROUND(SUM(amount), 0)
        FROM mart.fact_transaction
    )

UNION ALL

SELECT
    'fact_orphan_accounts',
    0,
    (
        SELECT COUNT(*)
        FROM mart.fact_transaction f
        LEFT JOIN mart.dim_account a
            ON a.account_sk = f.account_sk
        WHERE a.account_sk IS NULL
    )

UNION ALL

SELECT
    'dim_customer_dup_bk',
    0,
    (
        SELECT COUNT(*)
        FROM (
            SELECT customer_id
            FROM mart.dim_customer
            GROUP BY customer_id
            HAVING COUNT(*) > 1
        ) d
    );

