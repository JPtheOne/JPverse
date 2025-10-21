#!/usr/bin/env bash
set -e

echo "Starting JPverse deployment..."

# Step 1: Go to project directory
cd /root/JPverse || { echo "Project folder not found at /root/JPverse"; exit 1; }

# Step 2: Update repo
echo "Resetting local Git state to origin/main..."
git fetch && git reset origin/main --hard || { echo "Git fetch/reset failed."; exit 1; }

# Step 3: Stop running containers gracefully
echo "Stopping existing JPverse containers..."
if docker ps --format '{{.Names}}' | grep -q 'jpverse'; then
    docker-compose -f docker-compose.prod.yml stop || echo "Warning: stop failed but continuing..."
    docker-compose -f docker-compose.prod.yml rm -f || echo "Warning: rm failed but continuing..."
else
    echo "No existing JPverse containers found."
fi

# Step 4: Rebuild and start containers without removing shared networks
echo "Building and starting Docker containers..."
docker-compose -f docker-compose.prod.yml up -d --build || { echo "Docker Compose build failed."; exit 1; }

echo "Deployment complete. Containers are running."
