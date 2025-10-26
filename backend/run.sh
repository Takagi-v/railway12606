#!/bin/bash

# Railway 12306 Backend Startup Script

echo "Starting Railway 12306 Backend..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "Error: .env file not found. Please copy .env.example to .env and configure it."
    exit 1
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

