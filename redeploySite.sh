#!/usr/bin/env bash

echo "Starting JPverse deployment..."

# Step 1: Go to project directory
cd /root/JPverse || { echo "Project folder not found at /root/JPverse"; exit 1; }

# Step 2: Update repo
echo "Resetting local Git state to origin/main..."
git fetch && git reset origin/main --hard || { echo "Git fetch/reset failed."; exit 1; }

# Step 3: Stop running containers without removing shared networks
echo "Stopping existing Docker containers..."
docker-compose -f docker-compose.prod.yml stop || { echo "Failed to stop containers."; exit 1; }
docker-compose -f docker-compose.prod.yml rm -f || { echo "Failed to remove old containers."; exit 1; }

# Step 4: Rebuild and start
echo "Building and starting Docker containers..."
docker-compose -f docker-compose.prod.yml up -d --build || { echo "Docker Compose build failed."; exit 1; }

echo "Deployment complete. Containers are running."
