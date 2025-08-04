#!/bin/bash

# Check if the service "myportfolio" is up (no matter the actual container name)
if ! docker compose ps --services --filter "status=running" | grep -q "^myportfolio$"; then
    echo "Error: The service 'myportfolio' is not running."
    echo "Start it with: docker compose up -d"
    exit 1
fi

# Run the tests inside the service
docker compose exec myportfolio python -m unittest discover -s tests -p "test_*.py" -v
