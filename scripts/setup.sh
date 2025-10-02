#!/bin/bash
# Script to configure the development environment on Ubuntu

echo "=== Configuring Sheetwise - Development Environment ==="

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv .venv

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Update pip
echo "Updating pip..."
pip install --upgrade pip

# Install dependencies via poetry
echo "Installing dependencies..."
pip install poetry
poetry install

echo "=== Configuration complete! ==="
echo "To activate the virtual environment: source .venv/bin/activate"
echo "To run the application: python src/main.py"
