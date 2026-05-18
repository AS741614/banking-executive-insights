#!/bin/bash
set -e

# ESOTERIC Platform - VPS Bootstrapping Script
# This script prepares a generic Linux server for production deployment.

echo "--- Initializing ESOTERIC Platform Deployment ---"

# 1. Update system and install dependencies
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common gnupg lsb-release

# 2. Install Docker
if ! [ -x "$(command -v docker)" ]; then
    echo "Installing Docker..."
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io
    sudo usermod -aG docker $USER
fi

# 3. Install Docker Compose (v2)
if ! docker compose version > /dev/null 2>&1; then
    echo "Installing Docker Compose..."
    sudo apt-get install -y docker-compose-plugin
fi

# 4. Create directory structure for volumes
echo "Provisioning persistent volumes..."
mkdir -p data/prometheus_data data/grafana_data data/nginx/conf.d data/nginx/certs data/nginx/www

# 5. Initialize environment
if [ ! -f .env.production ]; then
    echo "Creating .env.production from example..."
    cp .env.production.example .env.production
    echo "WARNING: Please update .env.production with your institutional secrets before deploying."
fi

# 6. Deployment Command
echo "--- Preparation Complete ---"
echo "To deploy the platform, run:"
echo "docker compose -f docker/docker-compose.prod.yml --env-file .env.production up -d --build"

echo "--- SSL/TLS Recommendation ---"
echo "To enable SSL, install certbot and run:"
echo "sudo apt-get install certbot"
echo "sudo certbot certonly --webroot -w ./data/nginx/www -d yourdomain.com"
