# ESOTERIC Platform Deployment Guide

This directory contains the production-grade deployment infrastructure for the ESOTERIC BANK Intelligence Platform.

## Deployment Topology

The platform is designed for a **Hybrid Cloud Deployment**:
*   **Application Tier:** Hosted on a generic Linux VPS using Docker Compose.
*   **Database Tier:** Externalized to a DigitalOcean Managed PostgreSQL database for high availability and automated backups.
*   **Edge Tier:** Nginx reverse proxy handling TLS termination and routing.
*   **Observability Tier:** Integrated Prometheus and Grafana for institutional monitoring.

## Prerequisites

1.  **Generic Linux VPS:** Ubuntu 22.04 LTS or similar.
2.  **DigitalOcean Managed DB:** A PostgreSQL instance with connection URI ready.
3.  **Domain Name:** Pointed to the VPS IP address.

## Quick Start (VPS Deployment)

1.  **Clone the Repository** on the target server.
2.  **Bootstrap the Server:**
    ```bash
    chmod +x deployment/vps/setup.sh
    ./deployment/vps/setup.sh
    ```
3.  **Configure Environment:**
    Edit `.env.production` with your institutional secrets and the DigitalOcean `DWH_URL`.
4.  **Deploy the Stack:**
    ```bash
    docker compose -f docker/docker-compose.prod.yml --env-file .env.production up -d --build
    ```

## Security Hardening

*   **Non-Root Execution:** All application containers run as a dedicated `appuser`.
*   **Network Isolation:** Backend services (API, DB, Prometheus) are isolated from the public internet via internal Docker bridge networks.
*   **Edge Proxy:** Nginx implements strict security headers and TLS termination.
*   **Resource Limits:** Docker Compose enforces CPU and Memory caps to prevent noisy neighbor issues.

## Observability

*   **Grafana:** Accessible via `http://yourdomain.com/grafana` (default password in `.env.production`).
*   **Prometheus:** Scrapes telemetry from the API service automatically.
*   **Health Checks:** Both API and UI services include Docker health probes for automatic recovery.

## Maintenance & Scaling

*   **Scaling API:** Adjust `GUNICORN_WORKERS` in `.env.production` and restart the service.
*   **Logs:** Access logs via `docker compose -f docker/docker-compose.prod.yml logs -f`.
*   **Updates:** Pull latest changes and run the deploy command again with `--build`.
