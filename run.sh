#!/bin/bash

# Save Your Money - Startup Script

set -e  # Exit on any error

echo "🚀 Starting Save Your Money application..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Please run setup first."
    echo "Run: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Set environment variables
export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_DEBUG=true
if [ -z "$SECRET_KEY" ]; then
    export SECRET_KEY="dev-secret-key"
    echo "Using default SECRET_KEY. Set SECRET_KEY environment variable for production."
fi

# Check if database exists, if not initialize and migrate
if [ ! -f "website/database.db" ]; then
    echo "🗄️  Initializing database..."
    flask db init || echo "Database already initialized"
    flask db migrate -m "Initial migration" || echo "Migration failed"
    flask db upgrade
else
    echo "🗄️  Database exists, running upgrade if needed..."
    flask db upgrade || echo "No upgrades needed"
fi

# Start the application
echo "Starting Flask application on http://localhost:5000"
echo "Press Ctrl+C to stop"
python app.py