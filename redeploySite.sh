#!/usr/bin/env bash

echo "Starting JPverse deployment..."

# Step 1: Change to project directory
cd /root/JPverse || { echo "Project folder not found at /root/JPverse"; exit 1; }

# Step 2: Fetch and reset to latest code from origin/main
echo "Resetting local Git state to origin/main..."
git fetch && git reset origin/main --hard || { echo "Git fetch/reset failed."; exit 1; }

# Step 3: Stop containers to prevent memory issues
echo "Stopping existing Docker containers..."
docker-compose -f docker-compose.prod.yml down || { echo "Failed to stop containers."; exit 1; }

# Step 4: Rebuild and start containers
echo "Building and starting Docker containers..."
docker-compose -f docker-compose.prod.yml up -d --build || { echo "Docker Compose build failed."; exit 1; }

echo "Deployment complete. Containers are running."