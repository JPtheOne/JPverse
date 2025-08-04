#!/bin/bash

# Check if the container is running
if ! docker compose ps | grep -q "myportfolio.*Up"; then
    echo "Error: The container 'myportfolio' is not running."
    echo "Start it with: docker compose up -d"
    exit 1
fi

# Run tests inside the container
docker compose exec myportfolio python -m unittest discover -s tests -p "test_*.py" -v
