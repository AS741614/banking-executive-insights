CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS mart;

-- =========================
-- STAGING TABLES
-- =========================

CREATE TABLE IF NOT EXISTS staging.customers (
    customer_id INT,
    full_name TEXT,
    segment TEXT,
    country TEXT,
    onboarded_date DATE
);

CREATE TABLE IF NOT EXISTS staging.products (
    product_id INT,
    product_name TEXT,
    product_type TEXT
);

CREATE TABLE IF NOT EXISTS staging.branches (
    branch_id INT,
    branch_name TEXT,
    city TEXT,
    region TEXT
);

CREATE TABLE IF NOT EXISTS staging.accounts (
    account_id INT,
    customer_id INT,
    product_id INT,
    branch_id INT,
    open_date DATE,
    status TEXT
);

CREATE TABLE IF NOT EXISTS staging.transactions (
    txn_id BIGINT,
    account_id INT,
    txn_date DATE,
    txn_type TEXT,
    amount NUMERIC(14,2)
);

-- =========================
-- DIMENSIONS
-- =========================

CREATE TABLE IF NOT EXISTS mart.dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE NOT NULL,
    year INT,
    quarter INT,
    month INT,
    month_name TEXT,
    day INT,
    is_month_end BOOLEAN
);

CREATE TABLE IF NOT EXISTS mart.dim_customer (
    customer_sk SERIAL PRIMARY KEY,
    customer_id INT UNIQUE NOT NULL,
    full_name TEXT,
    segment TEXT,
    country TEXT,
    onboarded_date DATE
);

CREATE TABLE IF NOT EXISTS mart.dim_product (
    product_sk SERIAL PRIMARY KEY,
    product_id INT UNIQUE NOT NULL,
    product_name TEXT,
    product_type TEXT
);

CREATE TABLE IF NOT EXISTS mart.dim_branch (
    branch_sk SERIAL PRIMARY KEY,
    branch_id INT UNIQUE NOT NULL,
    branch_name TEXT,
    city TEXT,
    region TEXT
);

CREATE TABLE IF NOT EXISTS mart.dim_account (
    account_sk SERIAL PRIMARY KEY,
    account_id INT UNIQUE NOT NULL,
    customer_sk INT REFERENCES mart.dim_customer(customer_sk),
    product_sk INT REFERENCES mart.dim_product(product_sk),
    branch_sk INT REFERENCES mart.dim_branch(branch_sk),
    open_date DATE,
    status TEXT
);

-- =========================
-- FACT TABLES
-- =========================

CREATE TABLE IF NOT EXISTS mart.fact_transaction (
    txn_id BIGINT PRIMARY KEY,
    date_key INT REFERENCES mart.dim_date(date_key),
    account_sk INT REFERENCES mart.dim_account(account_sk),
    txn_type TEXT,
    amount NUMERIC(14,2) NOT NULL,
    signed_amount NUMERIC(14,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS mart.fact_account_month (
    account_sk INT REFERENCES mart.dim_account(account_sk),
    date_key INT REFERENCES mart.dim_date(date_key),
    net_flow NUMERIC(16,2),
    txn_count INT,
    PRIMARY KEY (account_sk, date_key)
);
