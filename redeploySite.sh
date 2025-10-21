#!/usr/bin/env bash
set -e

echo "Starting JPverse deployment..."

# Step 1: Go to project directory
cd /root/JPverse || { echo "Project folder not found at /root/JPverse"; exit 1; }

# Step 2: Update repo
echo "Resetting local Git state to origin/main..."
git fetch && git reset origin/main --hard || { echo "Git fetch/reset failed."; exit 1; }

# Step 3: Stop and remove only JPverse containers (not shared networks)
echo "Stopping existing JPverse containers..."
docker-compose -f docker-compose.prod.yml stop || echo "No containers to stop."

echo "Removing old JPverse containers (ignoring shared networks)..."
docker-compose -f docker-compose.prod.yml rm -f || echo "No containers to remove."

# 🔒 Protect shared network from removal errors
echo "Ensuring webnet exists..."
docker network inspect webnet >/dev/null 2>&1 || docker network create webnet || true

# Step 4: Rebuild and start fresh
echo "Building and starting JPverse containers..."
docker-compose -f docker-compose.prod.yml up -d --build || { echo "Docker Compose build failed."; exit 1; }

echo "✅ Deployment complete. JPverse containers are running."
