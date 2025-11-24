#!/bin/bash
# Setup development environment and run tests

set -e

echo "🔧 Setting up development environment..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Install package in editable mode
echo "Installing package in editable mode..."
pip install -e .

# Run tests with coverage
echo ""
echo "🧪 Running tests with coverage..."
pytest --cov=airflow_config --cov-report=html --cov-report=term-missing

echo ""
echo "✅ Setup complete! Coverage report available in htmlcov/index.html"
echo ""
echo "To activate the virtual environment manually:"
echo "  source venv/bin/activate"
