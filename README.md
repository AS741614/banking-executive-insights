# Banking Executive Insights

Enterprise Banking BI Platform using PostgreSQL, Python ETL, Tableau & CI/CD

---

# Overview

Banking Executive Insights is a governed business intelligence platform that transforms simulated banking source systems into a trusted analytical warehouse and executive reporting layer.

The project demonstrates enterprise-grade capabilities across:

- Data Engineering
- Warehouse Engineering
- ETL Orchestration
- Data Quality & Governance
- Performance Optimization
- BI Architecture
- DevOps & CI/CD Automation

The platform simulates realistic banking source systems and processes transactional data into a dimensional warehouse optimized for executive analytics and dashboard reporting.

---

# Architecture

text Synthetic Banking Systems         ↓ Raw CSV Layer         ↓ Staging Schema         ↓ Star Schema Warehouse         ↓ Fact Tables         ↓ Analytical Views         ↓ Materialized KPI Layer         ↓ Executive Dashboards 

---

# Technology Stack

| Layer | Technology |
|---|---|
| Database | PostgreSQL |
| ETL | Python + pandas + SQLAlchemy |
| Infrastructure | Docker |
| CI/CD | GitHub Actions |
| Analytics | SQL + Materialized Views |
| Data Quality | SQL Validation Framework |
| Visualization | Tableau |
| Orchestration | Makefile |
| Version Control | Git + GitHub |

---

# Key Features

## Synthetic Banking Source Systems

The platform generates realistic banking datasets including:

- Customers
- Accounts
- Banking Products
- Branches
- Transactions

Generated volumes:

| Dataset | Rows |
|---|---|
| Customers | 5,000 |
| Accounts | 8,000 |
| Transactions | 200,000 |
| Branches | 20 |
| Products | 5 |

---

# Enterprise ETL Pipeline

Implemented a fully automated ETL workflow:

text Extract → Stage → Transform → Load 

Pipeline capabilities:

- CSV ingestion
- Staging schema loading
- Dimensional transformations
- Fact table population
- Automated orchestration
- Idempotent warehouse loading

---

# Dimensional Warehouse Design

Implemented a star schema warehouse architecture with:

## Dimensions

- dim_customer
- dim_account
- dim_product
- dim_branch
- dim_date

## Fact Tables

- fact_transaction
- fact_account_month

Warehouse capabilities:

- Surrogate keys
- Transaction-level grain modeling
- Monthly snapshot aggregation
- Conformed dimensions
- Referential integrity

---

# Governance & Data Quality Framework

Implemented automated warehouse validation controls.

## Data Quality Checks

| Check | Purpose |
|---|---|
| Transaction Row Count Reconciliation | Prevent data loss |
| Transaction Amount Reconciliation | Financial integrity validation |
| Orphan Fact Detection | Referential integrity validation |
| Duplicate Business Key Detection | Dimensional consistency |

## Quality Gate

The pipeline automatically fails if any data quality rule breaks.

This simulates enterprise-grade governance controls used in regulated industries such as banking and financial services.

---

# Analytics & Performance Engineering

Implemented an analytical serving layer optimized for executive reporting.

## Optimization Features

- Indexed warehouse tables
- Analytical enriched views
- Materialized KPI aggregation layer
- Query optimization workflow
- Executive KPI serving architecture

## Analytical Objects

| Object | Purpose |
|---|---|
| vw_transaction_enriched | Detailed analytical exploration |
| mv_kpi_month | Fast executive KPI reporting |

## Performance Tuning

Implemented:

- Foreign key indexing
- Materialized aggregation strategy
- Query workload optimization
- Reduced dashboard query complexity

---

# DevOps & Automation

Implemented enterprise-style orchestration and automation.

## Dockerized Infrastructure

The PostgreSQL warehouse runs entirely in Docker containers.

## Makefile Automation

Entire platform execution is orchestrated through:

bash make all 

This automatically:

1. Starts infrastructure
2. Generates source data
3. Runs ETL pipeline
4. Executes data quality validation

## GitHub Actions CI/CD

Automated CI pipeline validates:

- Environment setup
- Dependency installation
- Source generation
- ETL execution
- Warehouse integrity
- Data quality rules

---

# Repository Structure

text banking-executive-insights/ ├── .github/workflows/ │ ├── data/raw/ │ ├── docs/ │   ├── data_dictionary.md │   ├── metric_definitions.md │   ├── data_lineage.md │   └── runbook.md │ ├── screenshots/ │ ├── sql/ │   ├── 01_schema.sql │   ├── 02_transform.sql │   ├── 03_analytics.sql │   └── 04_data_quality.sql │ ├── src/ │   ├── db.py │   ├── etl.py │   ├── generate_source_data.py │   └── run_quality_checks.py │ ├── tableau/ │ ├── docker-compose.yml ├── Makefile ├── requirements.txt ├── README.md └── .env.example 

---

# Quick Start

## Clone Repository

bash git clone https://github.com/AS741614/banking-executive-insights.git cd banking-executive-insights 

---

# Setup Python Environment

bash python -m venv .venv source .venv/bin/activate pip install -r requirements.txt 

---

# Run Full Platform

bash make all 

This automatically:

- Starts PostgreSQL
- Generates synthetic banking data
- Executes ETL pipeline
- Builds warehouse
- Runs data quality checks

---

# Example Pipeline Output

text Loaded branches → staging Loaded products → staging Loaded customers → staging Loaded accounts → staging Loaded transactions → staging  ETL pipeline completed successfully  All data quality checks passed 

---

# Business Use Cases

The platform supports:

- Executive KPI reporting
- Customer segment analysis
- Product performance analytics
- Regional banking performance
- Transaction flow analysis
- Operational banking insights

---

# Production Upgrade Path

Future enhancements planned:

- Tableau executive dashboard suite
- Slowly Changing Dimensions (SCD2)
- Incremental ETL loading
- Apache Airflow orchestration
- Partitioned warehouse tables
- Snowflake / BigQuery migration
- Real-time streaming ingestion
- Advanced KPI alerting

---

# Skills Demonstrated

| Capability | Demonstrated Through |
|---|---|
| SQL Engineering | Star schema + analytics layer |
| ETL Engineering | Automated warehouse pipeline |
| Warehouse Design | Fact/dimension modeling |
| Data Governance | Reconciliation framework |
| BI Engineering | KPI serving architecture |
| Performance Optimization | Materialized views + indexing |
| DevOps | Docker + CI/CD |
| Python Engineering | ETL orchestration |
| Data Quality | Automated validation gates |

---

# Why This Project Matters

Most analytics portfolios focus only on dashboards or notebooks.

This project demonstrates full-stack analytics engineering including:

- Infrastructure
- Warehouse architecture
- ETL orchestration
- Governance
- Performance optimization
- Automation
- Analytical serving design

The platform reflects real enterprise BI engineering patterns used in banking and regulated industries.

---

# Future Tableau Dashboard Suite

Planned dashboards include:

- Executive Overview Dashboard
- Customer & Segment Analytics
- Product Performance Dashboard
- Regional Branch Performance Dashboard
- KPI Trend & Flow Analysis

---

# Author

Akash Sharma

Data Analytics • BI Engineering • AI Systems • Enterprise Analytics


* operational runtime overview
* observability stack
* API endpoints
* Grafana credentials
* startup instructions
* crisis validation commands
* Docker runtime instructions
