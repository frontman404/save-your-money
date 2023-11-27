#!/bin/bash

# Save Your Money - Setup Script

set -e  # Exit on any error

echo "Setting up Save Your Money application..."

# Check Python version
python3 --version

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
else
    echo "Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Set environment variables for setup
export FLASK_APP=app.py
export FLASK_ENV=development
export SECRET_KEY="dev-secret-key"

# Initialize database
echo "Setting up database..."
if [ ! -d "migrations" ]; then
    flask db init
fi
flask db migrate -m "Initial setup"
flask db upgrade

echo "Setup complete!"
echo ""
echo "To run the application:"
echo "  ./run.sh"
echo ""
echo "Or manually:"
echo "  source .venv/bin/activate"
echo "  export FLASK_APP=app.py"
echo "  export SECRET_KEY='your-secret-key'"
echo "  python app.py"